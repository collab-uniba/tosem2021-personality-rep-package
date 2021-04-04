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
library(corrplot)

print("***************************************************")
print("*                     RQ0                         *")
print("***************************************************")

# config
set.seed(1977)
options(digits=3)

# load data
args = commandArgs(trailingOnly=TRUE)
infile <- if (length(args) < 1) 'data/final.csv' else args[1];
TEST <- if (length(args) == 2) TRUE else FALSE;
print("Loading data")
data <- read.csv(infile)

print("Rescaling and normalizing data")
# normalize
data$total_churn <- scale(log(data$total_churn + 1))
data$num_comments <- scale(bcPower(data$num_comments + 1,-1))
data$prior_interaction <- scale(log(data$prior_interaction + 1))
data$team_size <- scale(log(data$team_size + 1))
data$age_current <- scale(data$age_current + 1)
data$stars_current <- scale(log(data$stars_current + 1))
data$followers_current <- scale(log(data$followers_current + 1))
data$diff_openness_abs <- scale(log(data$diff_openness_abs + 1))
data$diff_agreeableness_abs <- scale(log(data$diff_agreeableness_abs + 1))
data$diff_conscientiousness_abs <- scale(log(data$diff_conscientiousness_abs + 1))
data$diff_extraversion_abs <- scale(log(data$diff_extraversion_abs + 1))
data$diff_neuroticism_abs <- scale(log(data$diff_neuroticism_abs + 1))
data$openness.x <- scale(log(data$openness.x + 1))
data$agreeableness.x <- scale(log(data$agreeableness.x + 1))
data$conscientiousness.x <- scale(log(data$conscientiousness.x + 1))
data$extraversion.x <- scale(log(data$extraversion.x + 1))
data$neuroticism.x <- scale(log(data$neuroticism.x + 1))
data$openness.y <- scale(log(data$openness.y + 1))
data$agreeableness.y <- scale(log(data$agreeableness.y + 1))
data$conscientiousness.y <- scale(log(data$conscientiousness.y + 1))
data$extraversion.y <- scale(log(data$extraversion.y + 1))
data$neuroticism.y <- scale(log(data$neuroticism.y + 1))

# remove file_changes due to high correlation with total_churn
data_pearson <- data
data_pearson$project_name <- NULL
data_pearson$owner <- NULL
data_pearson$name <- NULL
data_pearson$closer <- NULL
data_pearson$requester <- NULL
data_pearson$pull_req_id <- NULL
data_pearson$accepted <- NULL
data_pearson$openness.x <- NULL
data_pearson$conscientiousness.x <- NULL
data_pearson$extraversion.x <- NULL
data_pearson$agreeableness.x <- NULL
data_pearson$neuroticism.x <- NULL
data_pearson$openness.y <- NULL
data_pearson$conscientiousness.y <- NULL
data_pearson$extraversion.y <- NULL
data_pearson$agreeableness.y <- NULL
data_pearson$neuroticism.y <- NULL
data_pearson$diff_openness_abs <- NULL
data_pearson$diff_conscientiousness_abs <- NULL
data_pearson$diff_extraversion_abs <- NULL
data_pearson$diff_agreeableness_abs <- NULL
data_pearson$diff_neuroticism_abs <- NULL
cor(data_pearson, method = "spearman")

if(TEST == TRUE){
  data_s = dplyr::sample_n(data, 500)
  print("Working with a test subsample")
} else {
  data_s = data
  print("Working with the full dataset")
} 

print("Running logistic regression")
# logit from Iyer et al.
rq0 <- glmer(accepted ~ test_file 
             + total_churn  
             + social_distance 
             + num_comments 
             + prior_interaction 
             + followers_current 
             + main_team_member 
             + age_current 
             + team_size 
             + stars_current  
             + test_file*num_comments 
             + total_churn*num_comments 
             + social_distance*num_comments 
             + prior_interaction*num_comments 
             + (1|project_name) 
             + (1|requester) 
             + (1|closer), 
             data=data_s, family=binomial, 
             control = glmerControl(optimizer = "nloptwrap", calc.derivs = FALSE, optCtrl = list(maxeval = 300)));

# performance
AIC_rq0 <- round(AIC(rq0), digits = 2)
odds_ratio_rq0 <- round(exp(cbind(odds=fixef(rq0), 
                                  confint(rq0,parm="beta_",method="Wald", level = 0.99))), 2) 
index_rq0 <- r.squaredGLMM(rq0)

# comparison
Variables <- c("(Intercept)", "test_file", "total_churn", "files_changed", 
               "social_distance", "num_comments", "prior_interaction", 
               "followers_current", "main_team_member", "age_current", 
               "team_size", "stars_current", "test_file:num_comments", 
               "total_churn:num_comments", "file_changed:num_comments", 
               "social_distance:num_comments", "num_comments:prior_interaction", 
               "AIC")

Yver_et_al_replicated <- c(paste(odds_ratio_rq0[1:3], "(***)", sep=""),
                           "-", 
                           paste(odds_ratio_rq0[4:6], "(***)", sep=""),
                           odds_ratio_rq0[7], 
                           paste(odds_ratio_rq0[8], "(***)", sep=""), 
                           odds_ratio_rq0[9:10], 
                           paste(odds_ratio_rq0[11:13], "(***)", sep=""), 
                           "-", 
                           paste(odds_ratio_rq0[14:15], "(***)", sep=""), 
                           AIC_rq0)
Yver_et_al_original <- c("2.81", "1.08(***)", "0.9(***)", "-", "2.35(***)", 
                         "0.68(***)", "1.53(***)", "1.", "1.16(***)", 
                         "0.91(***)", "0.99", "0.53(***)", "1.12(***)", 
                         "1.06(***)", "-", "0.92(***)", "1.05(***)", "394718")
cbind(Variables, Yver_et_al_replicated, Yver_et_al_original)
print("Signif. codes:  ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1", quote = FALSE)
rowsname <- c("theoretical", "delta")
R2m_Yver_et_al <- round(index_rq0[0:2], 2)
R2c_Yver_et_al <- round(index_rq0[3:4], 2)
cbind(rowsname, R2m_Yver_et_al, R2c_Yver_et_al)