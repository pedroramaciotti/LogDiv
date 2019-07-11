import pandas as pd
import pydiv


###########################################
# Handling the arguments of the execution #
###########################################

# checking script was call correctly and retrieving
# the file with the parameters for the execution
#filename=file_functions.check_arguments(sys.argv) # temporary just for spyder
filename = 'parameters.yaml'
#############################################
# Retrieving execution parameters from file #
#############################################

# checking script was call correctly and retrieving
# the file with the parameters for the execution
parameters= pydiv.file_functions.read_parameters(filename)

# retrieving weblog columns, pages columns from parameters file
weblog_columns_dict  = pydiv.file_functions.retrieve_weblog_columns(parameters)
pages_columns_dict   = pydiv.file_functions.retrieve_pages_columns(parameters)
requests_threshold_per_session = parameters['session_data']['requests_threshold_per_session']

##############################################
# Reading the pages info file                #
##############################################
# page information file
pages=pd.read_csv(parameters['input_files']['pages_file'],low_memory=False)

################################################
# Reading weblog file, weblog tranform and     #
# sessionisation or loading pkl weblog file    #
################################################

# weblog file
weblog=pd.read_csv(parameters['input_files']['weblog_file'],low_memory=False).sort_values(by='timestamp')

# converting timestamp from strig to pandas timestamp
weblog[weblog_columns_dict['timestamp_column']]= pydiv.weblogtransform.pd_timestamp_convertor(weblog, weblog_columns_dict['timestamp_column'])

# Associating a session ID to each request
weblog['session_id'] = pydiv.weblogtransform.weblog_sessionizer(weblog,weblog_columns_dict,cutoff_minutes=30)

# deleting multiedges inside sessions
weblog.drop_duplicates(subset=[weblog_columns_dict['requested_page_column'],\
                               weblog_columns_dict['referrer_page_column'],'session_id'],inplace=True)

# including page classifications in log
weblog = pydiv.weblogtransform.assign_page_classification(weblog,pages,weblog_columns_dict,pages_columns_dict)

###############################################
# Session Table and Session Feature Space     #
###############################################
# retrieving features to be computed
session_features=pydiv.file_functions.retrieve_session_features(parameters)
# creating the session table
session_data = pd.DataFrame(columns=['session_id', 'userID', 'start', 'end']+session_features)

# Computing elemental session data
session_data['session_id'] = weblog.session_id.unique()
session_data['userID'] = session_data.session_id.map(weblog[['session_id',weblog_columns_dict['user_id_column']]].groupby('session_id').first()[weblog_columns_dict['user_id_column']])
session_data['start'] = session_data.session_id.map(weblog[[weblog_columns_dict['timestamp_column'], 'session_id']].groupby('session_id').min()[weblog_columns_dict['timestamp_column']])
session_data['end'] = session_data.session_id.map(weblog[[weblog_columns_dict['timestamp_column'], 'session_id']].groupby('session_id').max()[weblog_columns_dict['timestamp_column']])

# Computing session data features
session_data=pydiv.sessionfeatures.compute_session_features(weblog,pages,session_data,session_features,weblog_columns_dict, verbose = True)

# Filter sessions : >requests_threshold_per_session requests
session_data_threshold = session_data[session_data.requests > requests_threshold_per_session]

########################################
# Session Features Transformation      #
########################################

# retrieving features to be transformed for clusterisation
session_features=pydiv.file_functions.retrieve_session_features_transformed(parameters)
features_log_transform = pydiv.file_functions.retrieve_session_features_log_transformed(parameters)

# Computing session features transformation
session_features_t = [session_features[i]+'_t' for i in range(len(session_features))]
session_data_threshold[session_features_t] = pydiv.sessionspaces.session_transformation(session_data_threshold,session_features,features_log_transform,verbose = True)

# hist 1D of requests
pydiv.sessionspaces.plot_hist_requests(session_data,requests_threshold_per_session)


################################
# Cluster Computation          #
################################

# retrieving cluster_id with KMeans method
session_data_threshold['supervised_cluster_id_'] = pydiv.sessionspaces.supervised(session_data_threshold, session_features_t, n_cluster = 3, verbose = True)

#####################
# Group composition #
#####################

session_data['>4_requests'] = False
# > 4 requests
session_data.loc[session_data.requests > requests_threshold_per_session, '>4_requests'] = True

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
#proportion_data, entropy_matrix = pydiv.divanalysis.proportion_group(weblog, session_data,'requested_topic', pages.sport.unique(),['1_request','2_requests'],verbose = True)
#pydiv.divanalysis.plot_aggregated(proportion_data, entropy_matrix, requests_threshold_per_session)

# Temporal diversity
timeseries_data = pydiv.divanalysis.temporal_analysis(weblog,session_data,'requested_topic',parameters['temporal_filtering']['temporal_start'],\
                                                parameters['temporal_filtering']['temporal_end'],\
                                                ['1_request'], weblog_columns_dict,verbose = True)
#timeseries_data = pd.read_csv('/home/alexandre/Documents/Melty/Analysis/June_03__05/timeseries_data_June_03__05.csv')
pydiv.divanalysis.plot_temporal(timeseries_data,['1_request'],verbose = True)

# Classification diversity
browsing_matrix, markov_matrix, diversifying_matrix,change_browsing_matrix = pydiv.divanalysis.classification_diversity(weblog, pages.level.unique(), requests_threshold_per_session,verbose = True)

categories = pages.level.unique()
# plotting matrix
pydiv.divanalysis.plot_pattern_matrix(browsing_matrix,list(categories)+['marg.'],ticks_theme='greek',text_place='separate',\
                                xlabel='Browsing Matrix',verbose = True)
