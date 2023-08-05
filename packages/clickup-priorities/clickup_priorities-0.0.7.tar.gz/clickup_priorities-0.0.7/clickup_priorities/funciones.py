import requests
import datetime


def priorities(view_urls, authentication: dict):
    

    query_list =  [{"page": "1"},{"page": "2"},{"page": "3"}]
    results = {}


    def milliseconds_convertor(milliseconds):
        hour = ((milliseconds / 1000) / 60) / 60
        return round(hour, 1)


    def task_filter(task,sub_results, tasks_list, times_list):
        
        priority_id = task["priority"]["priority"]
        if task["time_estimate"] == None:
            time_millisecond = 0
        else:
            time_millisecond = task["time_estimate"]

        tasks_list.append([priority_id])
        times_list.append(milliseconds_convertor(time_millisecond))
        time_estimate = sum(times_list)

        task_dict = {priority_id: {"count": len(tasks_list), "time": time_estimate}}

        sub_results |= task_dict

        return sub_results


    for view in view_urls:

        url = "https://api.clickup.com/api/v2/view/" + view + "/task"
        
        response = requests.get(url, headers=authentication, params={"page": "0"})

        data = response.json()

        data_dict = dict(data)
        tasks = data_dict["tasks"]
        tasks_list = []     
        times_list = []
        
        if data_dict["last_page"] == False:
            
            page_sum = {}
            
            
            for task in tasks:
                sub_results = {}
                task_filter(task, sub_results, tasks_list, times_list)
                page_sum |= sub_results

            for i in query_list:
                response_page = requests.get(url, headers=authentication, params=i)
                data = response_page.json()
                data_dict = dict(data)
                tasks = data_dict["tasks"]

                for task in tasks:
                    task_filter(task, sub_results, tasks_list, times_list)
                    page_sum |= sub_results
                    
            results |= page_sum

        else:              
            for task in tasks:
                sub_results = {}
                task_filter(task, sub_results, tasks_list, times_list)
                results |= sub_results

    if response.status_code == 200:
        payload = {
            "date": datetime.datetime.today().strftime('%Y-%m-%d'),
            "urgent_count": results.get("urgent").get("count"),
            "urgent_time": results.get("urgent").get("time"),
            "high_count": results.get("high").get("count"),
            "high_time": results.get("high").get("time"),
            "normal_count": results.get("normal").get("count"),
            "normal_time": results.get("normal").get("time"),
            "low_count": results.get("low").get("count"),
            "low_time": results.get("low").get("time"),
        }
    else:
        payload = {
            "status code": response.status_code,
            "errors": response.raise_for_status()
        }

    return payload
