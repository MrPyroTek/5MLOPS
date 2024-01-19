# 5MLOPS

branch convention : 
- create your branch always from the develop branch.
- naming branch convention :
  - Feature Branches: feature/<feature-name>, e.g., feature/login-system
  - fix bugs or correction: fix/<bug-description>, e.g., bugfix/login-error
  - chore, for conf task or all thaht is not a bug or feature: chore/<issue>, e.g., hotfix/urgent-login-crash

commit convention :
- feat(<scope of the feature\>): message brief but usefull
  
Same convention than branches :
- feat
- fix
- chore

exemple : 
- feat(load data sript): add load data function
- chore(infra): upgrade memory of compute container

Merge request : 
Each branches must be merge on the develop branch before.
The convention naming is near to branch or commits. Add brief but a complete description to help reviewer to understand what you did.
Add reviewer.
