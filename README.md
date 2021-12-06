# Secret Santa

Dead simple website to help friends and family create a secret santa list, have others join it, and send out emails with the chosen recipients.
Features an exclusion option to not get selected for significant others or others in your household as well as a gift ideas list to help shopping easier. 
Check it out [here](https://santa.mitchmcaffee.com)!


## Project Structure

Serverless python backend in the root with a Vue frontend that lives in `/web`. Uses a single lambda and mailgun to send the emails. Deployed using
github actions to the aws resources defined in `serverless.yml`. Most of the AWS configuration is defined in `serverless.yml` but the config for Route53 is not.

### Deploy backend / frontend through CI

Simply push to the `main` branch and the code will be pushed to AWS using Github Actions.
