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

data <- read.csv('final.csv')


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


rq0 <- glmer(accepted ~ test_file + total_churn  + social_distance + num_comments + prior_interaction + followers_current + main_team_member + age_current + team_size + stars_current  + test_file*num_comments + total_churn*num_comments + social_distance*num_comments + prior_interaction*num_comments +  (1|project_name) + (1|requester) + (1|closer), data=data, family=binomial, control = glmerControl(optimizer = "nloptwrap", calc.derivs = FALSE, optCtrl = list(maxeval = 300)));

rq1 <- glmer(accepted ~ test_file + total_churn  + social_distance + num_comments + prior_interaction + followers_current + main_team_member + age_current + team_size + stars_current  + openness.x + conscientiousness.x + extraversion.x + agreeableness.x + neuroticism.x + test_file*num_comments + total_churn*num_comments + social_distance*num_comments + prior_interaction*num_comments + (1|project_name) + (1|requester) + (1|closer), data=data, family=binomial, control = glmerControl(optimizer = "nloptwrap", calc.derivs = FALSE, optCtrl = list(maxeval = 300)));

rq2 <- glmer(accepted ~ test_file + total_churn  + social_distance + num_comments + prior_interaction + followers_current + main_team_member + age_current + team_size + stars_current  + openness.y + conscientiousness.y + extraversion.y + agreeableness.y + neuroticism.y + test_file*num_comments + total_churn*num_comments + social_distance*num_comments + prior_interaction*num_comments + (1|project_name) + (1|requester) + (1|closer), data=data, family=binomial, control = glmerControl(optimizer = "nloptwrap", calc.derivs = FALSE, optCtrl = list(maxeval = 300)));

rq3 <- glmer(accepted ~ test_file + total_churn  + social_distance + num_comments + prior_interaction + followers_current + main_team_member + age_current + team_size + stars_current  +  diff_openness_abs + diff_conscientiousness_abs + diff_extraversion_abs + diff_agreeableness_abs + diff_neuroticism_abs + test_file*num_comments + total_churn*num_comments + social_distance*num_comments + prior_interaction*num_comments +  (1|project_name) + (1|requester) + (1|closer), data=data, family=binomial, control = glmerControl(optimizer = "nloptwrap", calc.derivs = FALSE, optCtrl = list(maxeval = 300)));
