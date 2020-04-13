def estimator(data):
  """ Provide the estimate calulations based on that data received """
  #Collect required data from data imput
  impact = {}
  severeImpact = {}
  reportedCases = data['reportedCases']
  periodType = data['periodType']
  timeToElapse = data['timeToElapse']
  totalHospitalBeds = data['totalHospitalBeds']
  avgDailyIncomeInUSD = data['region']['avgDailyIncomeInUSD']
  avgDailyIncomePopulation = data['region']['avgDailyIncomePopulation']



  # Conversion of the duration of the time elapse in day
  duration = get_duration_in_day(periodType, timeToElapse)
  factor = duration//3
  #-----
  #Result for Impact
  #CHALLENGE 1
  impact['currentlyInfected'] = reportedCases * 10
  impact['infectionsByRequestedTime'] = impact['currentlyInfected'] * (2**factor)

  #CHALLENGE 2
  impact['severeCasesByRequestedTime'] = int(impact['infectionsByRequestedTime'] * 0.15) 
  impact['hospitalBedsByRequestedTime'] = number_beds_avail(totalHospitalBeds, impact['severeCasesByRequestedTime'])

  #CHALLENGE 3
  impact['casesForICUByRequestedTime'] = int(impact['infectionsByRequestedTime'] * 0.05)
  impact['casesForVentilatorsByRequestedTime'] = int(impact['infectionsByRequestedTime'] * 0.02)
  impact['dollarsInFlight'] =int((impact['infectionsByRequestedTime'] * avgDailyIncomePopulation * avgDailyIncomeInUSD)/ duration)


  #--------------------------------------------------------------------------------------------------
  #Result for Severe Impact
  #CHALLENGE 1
  severeImpact['currentlyInfected'] = reportedCases * 50
  severeImpact['infectionsByRequestedTime'] = severeImpact['currentlyInfected']*(2**factor)

  #CHALLENGE 2
  severeImpact['severeCasesByRequestedTime'] = int(severeImpact['infectionsByRequestedTime'] * 0.15)
  severeImpact['hospitalBedsByRequestedTime'] = number_beds_avail(totalHospitalBeds, severeImpact['severeCasesByRequestedTime'])

  #CHALLENGE 3
  severeImpact['casesForICUByRequestedTime'] =  int(severeImpact['infectionsByRequestedTime'] * 0.05)
  severeImpact['casesForVentilatorsByRequestedTime'] = int(severeImpact['infectionsByRequestedTime'] * 0.02)
  severeImpact['dollarsInFlight'] = int((severeImpact['infectionsByRequestedTime'] * avgDailyIncomePopulation * avgDailyIncomeInUSD) /duration)


  result = {'data':data, 'impact':impact, 'severeImpact': severeImpact}

  return result

def get_duration_in_day(periodType, timeToElapse):
    """ Calculates the number of days in that period types received from the data input from the server """

    if periodType == "days":
        return timeToElapse
    elif periodType == "weeks":
        return timeToElapse * 7
    elif periodType == "months":
        return timeToElapse * 30
    else:
        return 0


def number_beds_avail(totalHospitalBeds, severeImpactCases):
    """ calculating the number of beds available as integers and not floats"""
    avail_beds = int((0.35 * totalHospitalBeds) - severeImpactCases)
    
    return avail_beds


