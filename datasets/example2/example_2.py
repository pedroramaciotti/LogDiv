import pandas as pd
import logdivv


###########################################
# Handling the arguments of the execution #
###########################################

# checking script was call correctly and retrieving
# the file with the parameters for the execution
#filename=file_functions.check_arguments(sys.argv) # temporary just for spyder
filename = 'parameters_2.yaml'
#############################################
# Retrieving execution parameters from file #
#############################################

# checking script was call correctly and retrieving
# the file with the parameters for the execution
parameters= logdivv.file_functions.read_parameters(filename)

# retrieving weblog columns, pages columns from parameters file
weblog_columns_dict  = logdivv.file_functions.retrieve_weblog_columns(parameters)
pages_columns_dict   = logdivv.file_functions.retrieve_pages_columns(parameters)
requests_threshold_per_session = parameters['session_data']['requests_threshold_per_session']

##############################################
# Reading the pages info file                #
##############################################
# page information file
pages=pd.read_csv(parameters['input_files']['pages_file'],low_memory=False)

# Selecting 6 most popular topic and category
categories = pages[pages_columns_dict['category_column']].value_counts().index[:6]
topics = pages[pages_columns_dict['topic_column']].value_counts().index[:6]

# Reclassifying categories and topics that won't be used in the analysis
pages[[pages_columns_dict['topic_column'],pages_columns_dict['category_column']]] = logdivv.weblogtransform.classifier(pages,topics,categories,pages_columns_dict)
################################################
# Reading weblog file, weblog tranform and     #
# sessionisation or loading pkl weblog file    #
################################################

# weblog file
weblog=pd.read_csv(parameters['input_files']['weblog_file'],low_memory=False).sort_values(by='timestamp')

# converting timestamp from strig to pandas timestamp
weblog[weblog_columns_dict['timestamp_column']]= logdivv.weblogtransform.pd_timestamp_convertor(weblog, weblog_columns_dict['timestamp_column'])

# Associating a session ID to each request
weblog['session_id'] = logdivv.weblogtransform.weblog_sessionizer(weblog,weblog_columns_dict,cutoff_minutes=30)

# deleting multiedges inside sessions
weblog.drop_duplicates(subset=[weblog_columns_dict['requested_page_column'],\
                               weblog_columns_dict['referrer_page_column'],'session_id'],inplace=True)

# including page classifications in log
weblog = logdivv.weblogtransform.assign_page_classification(weblog,pages,weblog_columns_dict,pages_columns_dict)

###############################################
# Session Table and Session Feature Space     #
###############################################
# retrieving features to be computed
session_features=logdivv.file_functions.retrieve_session_features(parameters)
# creating the session table
session_data = pd.DataFrame(columns=['session_id', 'userID', 'start', 'end']+session_features)

# Computing elemental session data
session_data['session_id'] = weblog.session_id.unique()
session_data['userID'] = session_data.session_id.map(weblog[['session_id',weblog_columns_dict['user_id_column']]].groupby('session_id').first()[weblog_columns_dict['user_id_column']])
session_data['start'] = session_data.session_id.map(weblog[[weblog_columns_dict['timestamp_column'], 'session_id']].groupby('session_id').min()[weblog_columns_dict['timestamp_column']])
session_data['end'] = session_data.session_id.map(weblog[[weblog_columns_dict['timestamp_column'], 'session_id']].groupby('session_id').max()[weblog_columns_dict['timestamp_column']])

# Computing session data features
session_data=logdivv.sessionfeatures.compute_session_features(weblog,pages,session_data,session_features,weblog_columns_dict, verbose = True)

# Filter sessions : >requests_threshold_per_session requests
session_data_threshold = session_data[session_data.requests > requests_threshold_per_session]

########################################
# Session Features Transformation      #
########################################

# retrieving features to be transformed for clusterisation
session_features=logdivv.file_functions.retrieve_session_features_transformed(parameters)
features_log_transform = logdivv.file_functions.retrieve_session_features_log_transformed(parameters)

# Computing session features transformation
session_features_t = [session_features[i]+'_t' for i in range(len(session_features))]
session_data_threshold[session_features_t] = logdivv.sessionspaces.session_transformation(session_data_threshold,session_features,features_log_transform,verbose = True)

# hist 1D of requests
logdivv.sessionspaces.plot_hist_requests(session_data,requests_threshold_per_session)


################################
# Cluster Computation          #
################################

# retrieving cluster_id with hierarchical method
list_features_t = [['requests_t','timespan_t'],['inter_req_sd_t','inter_req_mean_t']]
list_n_clusters = [3,2]
session_data_threshold['hierarchical_cluster_id'] = logdivv.sessionspaces.hierarchical(session_data_threshold, list_features_t,list_n_clusters, verbose = True)

session_data_pca, explained_variance_ratio, components = logdivv.sessionspaces.compute_pca(session_data_threshold, session_features_t, ['hierarchical_cluster_id'], verbose = True)
logdivv.sessionspaces.plot_explained_variance(explained_variance_ratio, threshold_explained_variance = 0.8, verbose = True)
# keep first and second Principal Components
logdivv.sessionspaces.scatterplot(session_data_pca, components[:2], session_features_t,'hierarchical_cluster_id', verbose = True)
logdivv.sessionspaces.scatterplot_centroids(session_data_pca,'hierarchical_cluster_id', components[:2], session_features_t,verbose=True)

#####################
# Group composition #
#####################
session_data['>4_requests'] = False
# >4 requests
session_data.loc[session_data.requests > 4, '>4_requests'] = True

session_data['4_requests'] = False
# 4 requests
session_data.loc[session_data.requests == 4, '4_requests'] = True

session_data['3_requests'] = False
# 3 requests
session_data.loc[session_data.requests == 3, '3_requests'] = True

session_data['2_requests'] = False
# 2 requests
session_data.loc[session_data.requests == 2, '2_requests'] = True

session_data['1_request'] = False
# 1 request
session_data.loc[session_data.requests == 1, '1_request'] = True

##########################
# Diversity analysis     #
##########################

# Aggregated diversity
proportion_data, entropy_matrix = logdivv.divanalysis.proportion_group(weblog, session_data,'requested_topic', pages[pages_columns_dict['topic_column']].unique(),['1_request','2_requests','3_requests','4_requests','>4_requests'],verbose = True)
logdivv.divanalysis.plot_aggregated(proportion_data, entropy_matrix)

# Temporal diversity
timeseries_data = logdivv.divanalysis.temporal_analysis(weblog,session_data,'requested_topic',parameters['temporal_filtering']['temporal_start'],\
                                                parameters['temporal_filtering']['temporal_end'],\
                                                ['2_requests','3_requests','>4_requests'], weblog_columns_dict,verbose = True)
logdivv.divanalysis.plot_temporal(timeseries_data,['2_requests','3_requests','>4_requests'],verbose = True)

# Classification diversity
browsing_matrix, markov_matrix, diversifying_matrix,change_browsing_matrix = logdivv.divanalysis.classification_diversity(weblog, categories, requests_threshold_per_session,verbose = True)


# plotting matrix
logdivv.divanalysis.plot_pattern_matrix(browsing_matrix,list(categories)+['marg.'],\
                                xlabel='Browsing Matrix',verbose = True)
logdivv.divanalysis.plot_pattern_matrix(markov_matrix,list(categories)+['marg.'],\
                                xlabel='Markov Matrix',verbose = True)
logdivv.divanalysis.plot_pattern_matrix(diversifying_matrix,list(categories)+['pt.'],\
                                xlabel='Diversifying Matrix',verbose = True)
logdivv.divanalysis.plot_pattern_matrix(change_browsing_matrix,list(categories)+['marg.'],\
                                xlabel='Change Browsing Matrix',verbose=True)
