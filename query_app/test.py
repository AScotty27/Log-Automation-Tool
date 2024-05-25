logset = {
    "logsets": [
        {
            "id": "23cf23a8-9b9b-4b6e-b45f-5cbd19544f28",
            "name": "test1",
            "description": "qwertyui",
            "user_data": {
                "hello": "world"
            },
            "logs_info": [
                {
                    "id": "89ed3b0d-2d9c-480b-9735-90c7d2f357c2",
                    "name": "myLog1",
                    "rrn": "rrn:logsearch:us:3a80d6bd-a051-43bf-a889-60cee58d8b41:logset:89ed3b0d-2d9c-480b-9735-90c7d2f357c2",
                    "links": {
                        "rel": "Self",
                        "href": "https://ap.rest.logs.insight.rapid7.com/log_search/management/logsets/89ed3b0d-2d9c-480b-9735-90c7d2f357c2"
                    }
                },
                {
                    "id": "89ed3b0d-2d9c-480b-9735-90c7d2f357c2",
                    "name": "myLog2",
                    "rrn": "rrn:logsearch:us:3a80d6bd-a051-43bf-a889-60cee58d8b41:logset:89ed3b0d-2d9c-480b-9735-90c7d2f357c2",
                    "links": {
                        "rel": "Self",
                        "href": "https://ap.rest.logs.insight.rapid7.com/log_search/management/logsets/89ed3b0d-2d9c-480b-9735-90c7d2f357c2"
                    }
                }
            ],
            "rrn": "rrn:logsearch:us:02abbff1-a1ed-452a-86eb-568bfb87e93e:log:022c2fc5-f9a0-4600-bd72-8d8d14bb1523"
        },
        {
            "id": "23cf23a8-9b9b-4b6e-b45f-5cbd19544f28",
            "name": "test2",
            "description": "qwertyui",
            "user_data": {
                "hello": "world"
            },
            "logs_info": [
                {
                    "id": "89ed3b0d-2d9c-480b-9735-90c7d2f357c2",
                    "name": "myLog1",
                    "rrn": "rrn:logsearch:us:3a80d6bd-a051-43bf-a889-60cee58d8b41:logset:89ed3b0d-2d9c-480b-9735-90c7d2f357c2",
                    "links": {
                        "rel": "Self",
                        "href": "https://ap.rest.logs.insight.rapid7.com/log_search/management/logsets/89ed3b0d-2d9c-480b-9735-90c7d2f357c2"
                    }
                },
                {
                    "id": "89ed3b0d-2d9c-480b-9735-90c7d2f357c2",
                    "name": "myLog2",
                    "rrn": "rrn:logsearch:us:3a80d6bd-a051-43bf-a889-60cee58d8b41:logset:89ed3b0d-2d9c-480b-9735-90c7d2f357c2",
                    "links": {
                        "rel": "Self",
                        "href": "https://ap.rest.logs.insight.rapid7.com/log_search/management/logsets/89ed3b0d-2d9c-480b-9735-90c7d2f357c2"
                    }
                }
            ],
            "rrn": "rrn:logsearch:us:02abbff1-a1ed-452a-86eb-568bfb87e93e:log:022c2fc5-f9a0-4600-bd72-8d8d14bb1523"
        }
    ]
}

print("=================")
logset_dict = {}
for logset in logset["logsets"]:
    for log in logset["logs_info"]:
        log_id = log['id']
        log_name = log['name']
        print(log_name, log_id)
        logset_dict[log_name] = log_id
print("=========dictionary=======")
print(logset_dict)
print("=================")
