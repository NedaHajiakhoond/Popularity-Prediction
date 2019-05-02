#import cl
#import argparse
import event_extraction
import read_weekly_comp

#ee = event_extraction.PopDataPreparation()
#ee.pop_data_preparation('166_active_forked_repos_list.csv')
#ee.get_repo_events_count('1','2015-01')
##ee.find_top_active_repositories(1000)

wc = read_weekly_comp.WeeklyData()
#wc.find_repo_creator('166_active_forked_repos_list.csv')
wc.find_weekly_comp('repos_creators.csv')