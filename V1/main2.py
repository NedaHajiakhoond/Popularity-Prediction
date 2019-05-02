#import cl
#import argparse
import event_extraction

ee = event_extraction.PopDataPreparation()
ee.pop_data_preparation('top_repos.csv')
#ee.get_repo_events_count('1','2015-01')
##ee.find_top_active_repositories(1000)