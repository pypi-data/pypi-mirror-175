import pandas as pd
import scipy.stats as stats

α = 0.05


def ReadData(dataset):
    dataset = pd.read_csv(dataset)
    return dataset


class Male:
    def __init__(self, dataset):
        self.dataset = dataset.loc[dataset['sex'] == 'Male']

    def Mean_bp(self):
        return self.dataset[['bp_before', 'bp_after']].mean()

    def T_test(self):
        return stats.ttest_rel(self.dataset['bp_before'], self.dataset['bp_after'])

    def Conclusion_Hypothesis(self):
        reject = ['Reject Null Hypothesis ❌',
                  'The drug is effective for male patient 😁']
        accept = ['Accept Null Hypothesis ✅',
                  'The drug is not effective for male patient ☹️']
        if self.T_test()[1] < α:
            return reject
        else:
            return accept


class Female:
    def __init__(self, dataset):
        self.dataset = dataset.loc[dataset['sex'] == 'Female']

    def Mean_bp(self):
        return self.dataset[['bp_before', 'bp_after']].mean()

    def T_test(self):
        return stats.ttest_rel(self.dataset['bp_before'], self.dataset['bp_after'])

    def Conclusion_Hypothesis(self):
        reject = ['Reject Null Hypothesis ❌',
                  'The drug is effective for female patient 😁']
        accept = ['Accept Null Hypothesis ✅',
                  'The drug is not effective for female patient ☹️']
        if self.T_test()[1] < α:
            return reject
        else:
            return accept
