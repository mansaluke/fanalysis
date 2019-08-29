#TODO: optimize rf
import pandas as pd
import numpy as np

try:
    import Random_Forest as r
    from Random_Forest import do_rf
except ImportError:
    import fanalysis.Models.Random_Forest as r
    from fanalysis.Models.Random_Forest import do_rf

class optimize_rf(do_rf):
    def __init__(self,
                df,
                indep_col = 'Bar OPEN Bid Quote',
                valid_size = 0.25,
                sample_random_state = 42,
                n_estimators=40,
                criterion="mse",
                max_depth=None,
                min_samples_split=2,
                min_samples_leaf=3,
                min_weight_fraction_leaf=0.,
                max_features=0.5,
                max_leaf_nodes=None,
                min_impurity_decrease=0.,
                min_impurity_split=None,
                bootstrap=True,
                oob_score=True,
                n_jobs=-1,
                random_state=None,
                verbose=0,
                warm_start=False):
        super().__init__(df,
                        indep_col,
                        valid_size,
                        sample_random_state,
                        n_estimators,
                        criterion,
                        max_depth,
                        min_samples_split,
                        min_samples_leaf,
                        min_weight_fraction_leaf,
                        max_features,
                        max_leaf_nodes,
                        min_impurity_decrease,
                        min_impurity_split,
                        bootstrap,
                        oob_score,
                        n_jobs,
                        random_state,
                        verbose,
                        warm_start)
        

    @property
    def opt_n_estimators(self):
        preds = self.tree_preds(graph=False)
        optimal  = pd.DataFrame(preds)[preds == max(preds)].reset_index()
        return min(optimal['index']) #optimal n_estimators
        


if __name__ == "__main__":
    
    df = dfc.df_store('EURUSD_tick_sample.h5', pathname, 'data').load_df()
    
    def test_split_df(df, prop = 0.25):
        df.sort_values(by=['Date'], inplace=True)
        return df[:round(len(df) *(1-prop))], df[round(len(df) * (1-prop)):]
    
    df, test = test_split_df(df)


    orf =  optimize_rf(df, n_estimators=100, indep_col = 'EURUSD.bid' )        
    opt_n_estimators = orf.opt_n_estimators
    rf = r.do_rf(df, n_estimators=opt_n_estimators, indep_col = 'EURUSD.bid')
    rf.predict_out(True)
    rf.return_error_details()
    rf.print_score()
    rf.importances()
    oosp = rf.out_of_sample_pred(test)


