from ProblemList import *
from ProblemLog import *

class User :
    def __init__ (self, user_id) :
        self.user_id = user_id
        self.get_problem_List()
        self.get_problem_log()

    def get_problem_List(self) :
        correct_list, wrong_list = ProblemList(self.user_id).get_problem_list()
        self.user_info_list = [self.user_id, correct_list, wrong_list]
        self.problem_list = correct_list + wrong_list
    
    def get_problem_log(self) :
        self.problem_info_list = ProblemLog(self.user_id, self.problem_list).do_crawling()

    def get_user_df(self) :
        user_info_df = pd.DataFrame(self.user_info_list).T
        user_info_df.columns=['user_id','correct_problem','wrong_problem']
        return user_info_df
    
    def get_problem_df(self) :
        user_problem_df=pd.DataFrame(self.problem_info_list)
        user_problem_df.columns=['user_id','problem_id','total_count','wrong_count', 'wrong_timeover', 'wrong_wrong', 'wrong_memoryover',
                                                        'memory','time','language','code_length','last_time']
        return user_problem_df