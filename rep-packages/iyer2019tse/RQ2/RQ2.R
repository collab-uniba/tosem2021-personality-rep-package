library(nortest)
library(car)
library(lme4)
library(moments)
library(effects)
library(sjstats)
library(sjPlot)
library(stringr)
require(MASS)
library(plyr)
library(tidyr)
library(Hmisc)
library(IRdisplay)
library(MuMIn)
library(boot)

print("***************************************************")
print("*                     RQ2                         *")
print("***************************************************")

# config
set.seed(1977)
options(digits=3)

# load data
args = commandArgs(trailingOnly=TRUE)
infile <- if (length(args) < 1) 'data/final_LIWC.csv' else args[1];
TEST <- if ((length(args) == 2) & args[2] == 'test') TRUE else FALSE;
print("Loading data")
data_pr <- read.csv(infile)

print("Rescaling and normalizing data")
data_pr$openness.x<-(data_pr$openness.x - min(data_pr$openness.x)) / (max(data_pr$openness.x) - min(data_pr$openness.x))
data_pr$agreeableness.x<-(data_pr$agreeableness.x - min(data_pr$agreeableness.x)) / (max(data_pr$agreeableness.x) - min(data_pr$agreeableness.x))
data_pr$conscientiousness.x<-(data_pr$conscientiousness.x - min(data_pr$conscientiousness.x)) / (max(data_pr$conscientiousness.x) - min(data_pr$conscientiousness.x))
data_pr$extraversion.x<-(data_pr$extraversion.x - min(data_pr$extraversion.x)) / (max(data_pr$extraversion.x) - min(data_pr$extraversion.x))
data_pr$neuroticism.x<-(data_pr$neuroticism.x - min(data_pr$neuroticism.x)) / (max(data_pr$neuroticism.x) - min(data_pr$neuroticism.x))
data_pr$openness.y<-(data_pr$openness.y - min(data_pr$openness.y)) / (max(data_pr$openness.y) - min(data_pr$openness.y))
data_pr$agreeableness.y<-(data_pr$agreeableness.y - min(data_pr$agreeableness.y)) / (max(data_pr$agreeableness.y) - min(data_pr$agreeableness.y))
data_pr$conscientiousness.y<-(data_pr$conscientiousness.y - min(data_pr$conscientiousness.y)) / (max(data_pr$conscientiousness.y) - min(data_pr$conscientiousness.y))
data_pr$extraversion.y<-(data_pr$extraversion.y - min(data_pr$extraversion.y)) / (max(data_pr$extraversion.y) - min(data_pr$extraversion.y))
data_pr$neuroticism.y<-(data_pr$neuroticism.y - min(data_pr$neuroticism.y)) / (max(data_pr$neuroticism.y) - min(data_pr$neuroticism.y))
data_pr$diff_openness_abs<-abs(data_pr$openness.x - data_pr$openness.y)
data_pr$diff_agreeableness_abs<-abs(data_pr$agreeableness.x - data_pr$agreeableness.y)
data_pr$diff_conscientiousness_abs<-abs(data_pr$conscientiousness.x - data_pr$conscientiousness.y)
data_pr$diff_extraversion_abs<-abs(data_pr$extraversion.x - data_pr$extraversion.y)
data_pr$diff_neuroticism_abs<-abs(data_pr$neuroticism.x - data_pr$neuroticism.y)

#normalize
data_pr$total_churn <- scale(log(data_pr$total_churn + 1))
data_pr$num_comments <- scale(bcPower(data_pr$num_comments + 1,-1))
data_pr$prior_interaction <- scale(log(data_pr$prior_interaction + 1))
data_pr$team_size <- scale(log(data_pr$team_size + 1))
data_pr$age_current <- scale(data_pr$age_current + 1)
data_pr$stars_current <- scale(log(data_pr$stars_current + 1))
data_pr$followers_current <- scale(log(data_pr$followers_current + 1))
data_pr$diff_openness_abs <- scale(log(data_pr$diff_openness_abs + 1))
data_pr$diff_agreeableness_abs <- scale(log(data_pr$diff_agreeableness_abs + 1))
data_pr$diff_conscientiousness_abs <- scale(log(data_pr$diff_conscientiousness_abs + 1))
data_pr$diff_extraversion_abs <- scale(log(data_pr$diff_extraversion_abs + 1))
data_pr$diff_neuroticism_abs <- scale(log(data_pr$diff_neuroticism_abs + 1))
data_pr$openness.x <- scale(log(data_pr$openness.x + 1))
data_pr$agreeableness.x <- scale(log(data_pr$agreeableness.x + 1))
data_pr$conscientiousness.x <- scale(log(data_pr$conscientiousness.x + 1))
data_pr$extraversion.x <- scale(log(data_pr$extraversion.x + 1))
data_pr$neuroticism.x <- scale(log(data_pr$neuroticism.x + 1))
data_pr$openness.y <- scale(log(data_pr$openness.y + 1))
data_pr$agreeableness.y <- scale(log(data_pr$agreeableness.y + 1))
data_pr$conscientiousness.y <- scale(log(data_pr$conscientiousness.y + 1))
data_pr$extraversion.y <- scale(log(data_pr$extraversion.y + 1))
data_pr$neuroticism.y <- scale(log(data_pr$neuroticism.y + 1))

if(TEST == TRUE){
  data_pr_s = dplyr::sample_n(data_pr, 1000)
  REP = 5
  print("Working with a test subsample")
} else {
  data_pr_s = data_pr
  REP = 50
  print("Working with the full dataset")
} 

print("Running logistic regression")
rq2_pr <- glmer(accepted ~ test_file 
                + total_churn  
                + social_distance 
                + num_comments 
                + prior_interaction 
                + followers_current 
                + main_team_member 
                + age_current 
                + team_size 
                + stars_current  
                + openness.y 
                + conscientiousness.y 
                + extraversion.y 
                + agreeableness.y 
                + neuroticism.y 
                + test_file*num_comments 
                + total_churn*num_comments 
                + social_distance*num_comments 
                + prior_interaction*num_comments 
                + (1|project_name) 
                + (1|requester) 
                + (1|closer), 
                data=data_pr_s, 
                family=binomial, 
                control = glmerControl(optimizer = "nloptwrap", 
                                       calc.derivs = FALSE, 
                                       optCtrl = list(maxeval = 300)));



AIC_rq2_pr <- round(AIC(rq2_pr), digits = 2) 
AIC_rq2_pr
odds_ratio_rq2_pr <- round(exp(cbind(odds=fixef(rq2_pr), confint(rq2_pr,parm="beta_",method="Wald", level = 0.99))), 2) # calcola odds ratio
odds_ratio_rq2_pr
index_rq2_pr <- r.squaredGLMM(rq2_pr) 
index_rq2_pr

# Bootstrap 95% CI for R-Squared
set.seed(42)
print("Bootstrapping")

regcoeff_pr <- function(formula, data, indices) { 
  d <- data[indices,] # allows boot to select sample 
  fit <- glmer(formula, 
               data=d, 
               family=binomial, 
               control = glmerControl(optimizer = "nloptwrap", 
                                      calc.derivs = FALSE,
                                      optCtrl = list(maxeval = 500)));
  return(exp(fixef(fit)))
}

closer_model_boot_pr <- boot(data=data_pr_s, 
                                statistic=regcoeff_pr, 
                                R=REP, 
                                formula=accepted ~ test_file 
                                + total_churn  
                                + social_distance 
                                + num_comments 
                                + prior_interaction 
                                + followers_current 
                                + main_team_member 
                                + age_current 
                                + team_size 
                                + stars_current  
                                + openness.y 
                                + conscientiousness.y 
                                + extraversion.y 
                                + agreeableness.y 
                                + neuroticism.y 
                                + test_file*num_comments 
                                + total_churn*num_comments 
                                + social_distance*num_comments 
                                + prior_interaction*num_comments 
                                + (1|project_name) 
                                + (1|requester) 
                                + (1|closer))

closer_model_boot_pr

print("Calculating 95% conf. int.")
for (i in 1:20){
  bci <-  boot.ci(closer_model_boot_pr, 
                  conf = 0.95, 
                  index=i, 
                  type=c("norm", "basic", "perc"))
  print(bci$normal)
}

print("Saving models to rda file")
save(rq2_pr, closer_model_boot_pr, file ="rep-packages/iyer2019tse/RQ2/bootstrap.rda")


