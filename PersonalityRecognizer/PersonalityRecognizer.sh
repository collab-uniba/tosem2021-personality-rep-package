#! /bin/bash -

# ENVIRONMENT VARIABLES

JDK_PATH=$JAVA_HOME/bin
WEKA=./weka-3-4/weka.jar

# ----------------------------------

COMMONS_CLI=./lib/commons-cli-1.0.jar
MRC=./lib/jmrc.jar

LIBS=.:$WEKA:$COMMONS_CLI:$MRC:bin/

$JDK_PATH/java -Xmx512m -classpath $LIBS recognizer.PersonalityRecognizer $*
