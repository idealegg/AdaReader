antlr4 ADA95.g4
javac *.java
grun ADA95 compilation -token -trace ../iac_flight_plan_types.a 2>&1|tee tmp.log