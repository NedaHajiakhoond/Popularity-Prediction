from pymongo import MongoClient
import urllib.parse
import ssl
import pandas as pd
import time
import gc
import json
import os
import shutil
import pathlib

class PopDataPreparation:
	
	def __init__(self):
		self.pre_months = [
		          "2015-01", "2015-02", "2015-03", "2015-04", "2015-05", "2015-06",
		          "2015-07", "2015-08", "2015-09", "2015-10", "2015-11", "2015-12",
		          "2016-01", "2016-02", "2016-03", "2016-04", "2016-05", "2016-06",
		          "2016-07", "2016-08", "2016-09", "2016-10", "2016-11", "2016-12",
		          "2017-01", "2017-02"]

		self.months = [ "2015-12-3", "2016-01-0","2016-01-1", "2016-01-2","2016-01-3", "2016-02-0","2016-02-1", "2016-02-2","2016-02-3", "2016-03-0","2016-03-1", "2016-03-2","2016-03-3", "2016-04-0","2016-04-1", "2016-04-2","2016-04-3",
		           "2016-05-0","2016-05-1", "2016-05-2","2016-05-3", "2016-06-0","2016-06-1", "2016-06-2","2016-06-3", "2016-07-0","2016-07-1", "2016-07-2","2016-07-3", "2016-08-0","2016-08-1", "2016-08-2","2016-08-3","2016-09-0","2016-09-1", "2016-09-2","2016-09-3", "2016-10-0","2016-10-1", "2016-10-2","2016-10-3", "2016-11-0","2016-11-1", "2016-11-2","2016-11-3","2016-12-0","2016-12-1", "2016-12-2","2016-12-3"
		           ,"2017-01-0","2017-01-1", "2017-01-2","2017-01-3", "2017-02-0","2017-02-1", "2017-02-2","2017-02-3", "2017-03-0","2017-03-1", "2017-03-2","2017-03-3", "2017-04-0","2017-04-1", "2017-04-2","2017-04-3",
		           
		           "2017-05-0","2017-05-1", "2017-05-2","2017-05-3", "2017-06-0","2017-06-1", "2017-06-2","2017-06-3", "2017-07-0","2017-07-1", "2017-07-2","2017-07-3", "2017-08-0","2017-08-1", "2017-08-2","2017-08-3","2017-09-0","2017-09-1", "2017-09-2","2017-09-3", "2017-10-0","2017-10-1", "2017-10-2","2017-10-3", "2017-11-0","2017-11-1", "2017-11-2","2017-11-3","2017-12-0","2017-12-1", "2017-12-2","2017-12-3"]    

		self.test_months = ["2016-01", "2016-02", "2016-03", "2016-04", "2016-05", "2016-06",
		          "2016-07", "2016-08", "2016-09", "2016-10", "2016-11", "2016-12"]
		
		self.eventTypes = ["WatchEven","PullRequestEvent" , "ForkEvent", "IssuesEvent","CommitCommentEvent", "IssueCommentEvent", "CreateEvent","PushEvent"]
		
		
		
		user =urllib.parse.quote_plus("nbidoki")
		pw = urllib.parse.quote_plus("NBidokiS0cialS1m")
		uri = "mongodb://%s:%s@10.0.2.153:27017/?authMechanism=SCRAM-SHA-1" % (user, pw)
		client = MongoClient(uri,
							 ssl=True,
							 ssl_cert_reqs=ssl.CERT_NONE)
		print("Start")
		
		#db_name = "top-1000-users"
		db_name = "github-training"
		self.db = client[db_name]
	
	def get_repo_events_count(self,repo,month):
	    month_regex = "^%s*" % month
	    #print("Querying", month_regex)
	    query_start_time = time.time()
	    query_results = self.db.Events.aggregate([
	        {"$match": {"created_at": {"$regex": month_regex},"repo.name_h": repo,"type": "WatchEvent"}}
	        ,
	        {
	            "$group": {
	                "_id": {"name_h": "$repo.name_h"},
	                "%s" %month: {"$sum": 1}
	            }
	        }
	    ]
	        ,
	        allowDiskUse=True
	    )
	    query_time_len = (time.time() - query_start_time) / 60.0
	    #print("Query execution time:\t%.2f" % query_time_len)
	
	    df = pd.DataFrame(list(query_results))
	    #print(df.head())
	    #print("Flattening ...")
	    if(not df.empty):
	    	df = pd.concat([df.drop(["_id"], axis=1), df["_id"].apply(pd.Series)], axis=1)
	    else:
	    	df=pd.DataFrame(data={'name_h':repo, '%s' %month: '0'}, index=[0])
	    return df
	
	def find_top_active_repositories(self, top):
		query_results = self.db.Events.aggregate([
		{
		"$group":
			{
			"_id": "$repo.name_h",
			"count": {"$sum": 1}
			}
		}
		,
		{
		"$sort":
			{
				"count": -1
			}
		}
		,
		{
		"$limit" : top
		}
		]
		,
		allowDiskUse=True
		)
		active_repos_df = pd.DataFrame(list(query_results))
		active_repos_df= pd.concat([active_repos_df.drop(["_id"], axis=1), active_repos_df["_id"].apply(pd.Series)], axis=1)
		active_repos_df.to_csv("top_repos.csv")

    
	def pop_data_preparation(self,fl):
		print('watch')
		repos = pd.read_csv(fl,nrows=100)
		repos_list=repos['name_h'].tolist()
		print(len(repos_list))
		#all_data = pd.DataFrame(columns=['name_h'])
		for m in self.months:
			print(m)
			start_time = time.time()
			month_df = pd.DataFrame(columns=['%s'%m,'name_h'])
			for i,repo in enumerate(repos_list):
				print(i)
				df = self.get_repo_events_count(repo,m)
				#print('len(df):', len(df))
				#print('df.columns:',df.columns)
				#print('month_df.columns:',month_df.columns)
				month_df=month_df.append(df)
				#print('month_df:',month_df)
				#pd.concat([df,month_df],ignore_index = True)
			month_df.to_csv("10days166-100repos-watch/%s.csv"%m)
			query_time_len = (time.time() - start_time) / 60.0
			print("month execution time:\t%.2f" % query_time_len)
			#print('month: ',len(month_df))
			#if (all_data.empty):
			#	all_data=month_df[['name_h','%s'%m]]
			#else:
			#	all_data = pd.merge(all_data, month_df, on='name_h')
		#print('all_data: ',len(all_data))
		#all_data.to_csv("test_all.csv")
		
def get_repo_events_count(self,repo,month):
	    month_regex = "^%s*" % month
	    #print("Querying", month_regex)
	    query_start_time = time.time()
	    query_results = self.db.Events.aggregate([
	        {"$match": {"created_at": {"$regex": month_regex},"repo.name_h": repo,"type": "WatchEvent"}}
	        ,
	        {
	            "$group": {
	                "_id": {"name_h": "$repo.name_h"},
	                "%s" %month: {"$sum": 1}
	            }
	        }
	    ]
	        ,
	        allowDiskUse=True
	    )
	    query_time_len = (time.time() - query_start_time) / 60.0
	    #print("Query execution time:\t%.2f" % query_time_len)
	
	    df = pd.DataFrame(list(query_results))
	    #print(df.head())
	    #print("Flattening ...")
	    if(not df.empty):
	    	df = pd.concat([df.drop(["_id"], axis=1), df["_id"].apply(pd.Series)], axis=1)
	    else:
	    	df=pd.DataFrame(data={'name_h':repo, '%s' %month: '0'}, index=[0])
	    return df
	
		