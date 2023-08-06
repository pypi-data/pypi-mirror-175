This CLI app is made for saved palettes analysis. There are various commands to get weekly/monthly/daily saved palette results and compare them. To get the full potential of the app, please read this guide.

Notes
1. Throughout this note, commands to be run will be written inside double quotes. You should run the commands without the double quotes.
2. The API key will be denoted as "XYXYXY". You should always replace it with your actual API key for Unhidden Beauty.
3. Every command starts with "unhidden", as it's the name of the app.
4. Before using the app for the first time, you need to download the API data to your local machine. To do that, simply run "unhidden api XYXYXY --update".
4. Every time you want to do a new analysis (e.g., weekly metrics update), you need to first update your local data so that it stores the latest saved palettes as well. So, make a habbit to run "unhidden api XYXYXY --update" everytime you want to use the app. It will take only a couple of seconds.


All Commands

1. api
api command is for accessing general info about saved palettes API. Run "unhidden api XYXYXY" to simply run it and learn when you updated your local data last time.

2. palette
palette command is for analyzing saved palettes metrics for different time periods. You can give any starting and ending date of format "dd.mm.yy" and it will return the results. 

Example usages of "palette" command:
> unhidden palette 5.10.22 12.10.22 (returns saved palette metrics for the given period including October 12th)
> unhidden palette 2.6.22 now (returns metrics from February 2th up to now)
> unhidden palette today (returns today's metrics)
> unhidden palette yesterday (returns yesterday's metrics)
> unhidden palette lastweek (returns metrics of last full week)

Add the argument "--compare" to compare the metrics to the previous time interval of same length. Examples:
> unhidden palette 1.10.22 31.10.22 --compare (returns october's metrics and also compares it with september)
> unhidden palette lastweek --compare (returns last full week's metrics and also compares it with previous week)

Add the argument "--count" to get the list of people that saved specific amount of palettes. Examples:
> unhidden palette lastweek --count '3' (returns list of users who saved exactly 3 palettes last week. Make sure to include single quotes)
> unhidden palette 1.1.21 31.1.21 --count '>5' (returns list of users who saved more than 5 palettes in January 2021)

3. customer-wc
customer-wc command is for getting the users of interest and also getting "Customer WC" sheets for engagement data of any week. Since this command modifies the Shopify report, make sure to download it from Shopify first. In order to download the report, log in to Shopify, go to "Analytics > Reports". Open the report named "
First time and return customers _ excluding tests _KS_updated_250722". Set the dates you want to be analyzed and make sure data is displayed "Daily". Then click "Export" and export data as CSV file. It will be on your downloads folder. Now you're ready to run this command.

Examples:
> unhidden customer-wc 7.11.22 (returns users of interest for week commencing November 7th, and also updates Shopify report of same date range)

Add the argument "--month" to get monthly data instead of weekly. Examples:
> unhidden customer-wc 1.11.22 --month

4. palette-wc
palette-wc command is for getting palettes information for the sheet "Saved palettes WC" for engagement sheets. Simplly run this command and then the data will be copied to your keyboard. Then paste it to the sheet.

Example usage:
> unhidden palette-wc 7.11.22

Add "--save" argument to save the data as csv file instead.
Example:
> unhidden palette-wc 7.11.22 --save
