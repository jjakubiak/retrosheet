

### add loop with week star and week end dates

if __name__ == "__main__":
    exec(open("api_request.py").read())     # api request for raw json
    exec(open("transform.py").read())       # process and transform raw json
    exec(open("combine_data.py").read())    # combine individual data files and move into complete folder

    # exec(open("feature_engineer.py").read())
    # exec(open("model.py").read())