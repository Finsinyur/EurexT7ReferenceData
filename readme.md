# Getting Eurex T7 Reference Data using GraphQL

This is a documentation on how to access Eurex T7 Reference data using Python.
Please refer to the following blog post for full instructions:
https://medium.com/analytics-vidhya/get-eurex-trading-holidays-and-more-in-5-mins-using-python-and-graphql-c4fdec4f4417

Eurex T7 Reference data is available via GraphQL API: https://console.developer.deutsche-boerse.com/apis/accesstot7-referencedata/1.1.0.

GraphQL is a front-end API that can be accessed via a Google Chrome Extension. However, this would not be very useful as users are unable to incorporate these data into their own programs. This project thus seeks to provide readers with a solution to connect Python to GraphQL.

Beyond showing how one can retrieve data via Python, this project also displays some of the interesting data available on this API. Some information explored here is the Basic Product Information and Trading Holidays. This can be further expanded to Trading Hours and other interesting product specifications.

For more information on the API provided by Deutsche Boerse Group, please refer to https://console.developer.deutsche-boerse.com/.
For more information on GraphQL, please refer to the documentation here: https://graphql.org/learn/. 
