import pandas as pd
import logdiv


# retrieve YAML file
filename = 'parameters_1.yaml'
parameters= logdiv.file_functions.read_parameters(filename)

# retrieving weblog columns, pages columns from parameters file
weblog_columns_dict  = logdiv.file_functions.retrieve_weblog_columns(parameters)
pages_columns_dict   = logdiv.file_functions.retrieve_pages_columns(parameters)
requests_threshold_per_session = parameters['session_data']['requests_threshold_per_session']

# page information file
pages=pd.read_csv(parameters['input_files']['pages_file'],low_memory=False)

# weblog file
weblog=pd.read_csv(parameters['input_files']['weblog_file'],low_memory=False).sort_values(by='timestamp')

# converting timestamp from strig to pandas timestamp
weblog[weblog_columns_dict['timestamp_column']]= logdiv.weblogtransform.pd_timestamp_convertor(weblog, weblog_columns_dict['timestamp_column'])

# Associating a session ID to each request
weblog['session_id'] = logdiv.weblogtransform.weblog_sessionizer(weblog,weblog_columns_dict,cutoff_minutes=30)

# deleting multiedges inside sessions
weblog.drop_duplicates(subset=[weblog_columns_dict['requested_page_column'],\
                               weblog_columns_dict['referrer_page_column'],'session_id'],inplace=True)

# including page classifications in log
weblog = logdiv.weblogtransform.assign_page_classification(weblog,pages,weblog_columns_dict,pages_columns_dict)

# retrieving features to be computed
session_features=logdiv.file_functions.retrieve_session_features(parameters)
# creating the session table
session_data = pd.DataFrame(columns=['session_id', 'userID', 'start', 'end']+session_features)

# Computing elemental session data
session_data['session_id'] = weblog.session_id.unique()
session_data['userID'] = session_data.session_id.map(weblog[['session_id',weblog_columns_dict['user_id_column']]].groupby('session_id').first()[weblog_columns_dict['user_id_column']])
session_data['start'] = session_data.session_id.map(weblog[[weblog_columns_dict['timestamp_column'], 'session_id']].groupby('session_id').min()[weblog_columns_dict['timestamp_column']])
session_data['end'] = session_data.session_id.map(weblog[[weblog_columns_dict['timestamp_column'], 'session_id']].groupby('session_id').max()[weblog_columns_dict['timestamp_column']])

# Computing session data features
session_data=logdiv.sessionfeatures.compute_session_features(weblog,pages,session_data,session_features,weblog_columns_dict, verbose = True)

# Filter sessions : >requests_threshold_per_session requests
session_data_threshold = session_data[session_data.requests > requests_threshold_per_session]

# retrieving features to be transformed for clusterisation
session_features=logdiv.file_functions.retrieve_session_features_transformed(parameters)
features_log_transform = logdiv.file_functions.retrieve_session_features_log_transformed(parameters)

# Computing session features transformation
session_features_t = [session_features[i]+'_t' for i in range(len(session_features))]
session_data_threshold[session_features_t] = logdiv.sessionspaces.session_transformation(session_data_threshold,session_features,features_log_transform,verbose = True)

# hist 1D of requests
logdiv.sessionspaces.plot_hist_requests(session_data,requests_threshold_per_session)

# retrieving cluster_id with KMeans method
session_data_threshold['supervised_cluster_id_'] = logdiv.sessionspaces.supervised(session_data_threshold, session_features_t, n_cluster = 3, verbose = True)

# Group composition
session_data['>2_requests'] = False
# >1 requests
session_data.loc[session_data.requests > 2, '>2_requests'] = True

session_data['2_requests'] = False
# 2 requests
session_data.loc[session_data.requests == 2, '2_requests'] = True

# Aggregated diversity
proportion_data, entropy_matrix = logdiv.divanalysis.proportion_group(weblog, session_data,'requested_topic',\
                                                                      pages[pages_columns_dict['topic_column']].unique(),['2_requests','>2_requests'],verbose = True)
logdiv.divanalysis.plot_aggregated(proportion_data, entropy_matrix, requests_threshold_per_session)

# Classification diversity
browsing_matrix, markov_matrix, diversifying_matrix,change_browsing_matrix = \
            logdiv.divanalysis.classification_diversity(weblog, pages[pages_columns_dict['category_column']].unique(), requests_threshold_per_session,verbose = True)

categories = pages[pages_columns_dict['category_column']].unique()
# plotting matrix
logdiv.divanalysis.plot_pattern_matrix(browsing_matrix,list(categories)+['marg.'],\
                                xlabel='Browsing Matrix',verbose = True)
