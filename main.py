import time
import requests
import numpy
import matplotlib.pyplot as plt

# https://www.quandl.com/

# Student 
# Name:     Petur Einarsson
# ID:       160990447

#==============================================================================
""" Control panel: """
#==============================================================================
# The below variables can be changed for different results

apiKEY      = ''
dataFormat  = 'csv'   # 'json' or 'csv'

stock           = 'APPL'
startDate       = "2016-12-30"
endDate         = "2016-12-30"
requestCount    = 1000






#==============================================================================
# Initiate variables
#==============================================================================

# Format API url
baseURL     = "https://www.quandl.com/api/v3/datasets/"
dataType    = '.' + dataFormat + '?'
dateRange   = "start_date=" + startDate + "&end_date=" + endDate
api_key     = "&api_key=" + apiKEY
FULL_URL = baseURL + stock + dataType + dateRange + api_key

# Set API request limits
# http://help.quandl.com/article/68-is-there-a-rate-limit-or-speed-limit-for-api-usage
# Anonymous Users 	    20   calls / 10 minutes (600 seconds)
# Logged-In Free Users    2000 calls / 10 minutes (600 seconds)
# Premium Subscribers 	    5000 calls / 10 minutes (600 seconds)

APILimit        = 2000    # MAX number of calls
APITimeLimit    = 600    # MAX time limit in seconds

interval                = 1
response_times          = []

requestLimit        = APILimit     * interval
requestTimeLimit    = APITimeLimit * interval
#============================================================================== 
""" MAIN function """
#============================================================================== 
beginTime = time.time()    # start timer

timeTaken = []
for request in range(requestCount):
    startTime = time.time()
    print("Request #",request)

    currentRequest = requests.get(FULL_URL)
    currentRequest.content   # wait for response from above function
    
    currentTime = time.time()
    requestStartTimeLim = currentTime - beginTime
    
    endTime = time.time()
    
    requestDuration = endTime - startTime
    timeTaken.append(requestDuration)
    
    if (request == requestLimit) and (requestStartTimeLim < requestTimeLimit):
        sleepTime = requestTimeLimit - requestStartTimeLim
        print("Request limit reached")
        print("Sleeping for:", sleepTime, "seconds")
        time.sleep(sleepTime)
        interval += 1
#==============================================================================
""" Metrics """
#==============================================================================
arr = numpy.array(timeTaken)

print("Average response time:",numpy.mean(arr, axis=0) )
print("Median  response time:",numpy.median(arr, axis=0) )
print("MIN     response time:",numpy.min(arr, axis=0) )
print("MAX     response time:",numpy.max(arr, axis=0) )
print("Std     response time:",numpy.std(arr, axis=0) )

plt.hist(arr, bins='auto')  # plt.hist passes it's arguments to np.histogram
plt.title("Response time distribution")
plt.show()
#==============================================================================
endTime = time.time()
totalTime = endTime - beginTime

print("\nTotal Runtime:   ",totalTime)
print("Number of requests:", requestCount)