from flask import Flask, request, render_template, jsonify, abort, session
import sys, os
import boto3
import uuid
import json
import datetime
from time import sleep

awskey = os.getenv("AWS_ACCESS_KEY_ID")
awsskey = os.getenv("AWS_SECRET_ACCESS_KEY")

sns = boto3.client("sns", region_name="eu-north-1", aws_access_key_id=awskey, aws_secret_access_key=awsskey)
dn = boto3.client("dynamodb", region_name="eu-north-1", aws_secret_access_key=awsskey, aws_access_key_id=awskey)

app = Flask(__name__, static_folder="static", template_folder="templates")
app.secret_key = os.urandom(32)

@app.route("/", methods=["GET", "POST"])
def e():
    if request.method == "GET" and not request.headers.get("Referer"): 
        return render_template("index.html")

    if request.method == "GET" and request.headers.get("Referer"): 
        print("Checking it...", end="\n\n")

        email = session.get("email")
        topicarn = session.get("topicarn")

        subscript = sns.list_subscriptions_by_topic(TopicArn=topicarn)

        confirmat = next(("True" for i in subscript["Subscriptions"] if i["SubscriptionArn"].startswith("arn") and i["Endpoint"] == email), None)
        print("confirmat: ", confirmat)

        return jsonify({"Status": "A" if confirmat else "F"}), 200

    if request.method == "POST":
        print(20 * "-")

        email = request.form.get("emailf")
        print("email: ", email)
        text = request.form.get("textf")

        try:
            topiclist = sns.list_topics().get("Topics")
            topicarn = topiclist[-1]["TopicArn"]
            session["topicarn"] = topicarn

            print("topicarn: ", topicarn, end="\n\n")

            if not topiclist:
                print("Topic has been created", end="\n\n")
                sns.create_topic(Name=str(uuid.uuid4()))

        except Exception as e:
            print("An error occurred: ", str(e))
            return jsonify({"status": "error", "message": str(e)}), 500

        session["email"] = email

        topicarn = topiclist[-1]["TopicArn"]
        subscript = sns.list_subscriptions_by_topic(TopicArn=topicarn)
        print("email: ", email)

        arndl = [i for i in subscript["Subscriptions"] if i["SubscriptionArn"].startswith("arn")]

#These loops below likely will not traverse over the list since there will be a single element in the list(arndl) for the subscription 


        arndlcp = next((i["SubscriptionArn"] for i in arndl if i["Endpoint"] != email), None) #Checks if there any confirmed subscription


        arndlc = next((i for i in arndl if i["Endpoint"] == email), None) if not arndlcp else False #Checks if the email has already confirmed


        print("arndl: ", arndl, "arndlcp: ", arndlcp, "arndlc: ", arndlc, sep="\n") 
        print("Topiclist: ", topiclist, "subscript: ", subscript, sep="\n", end="\n\n") 

        if arndlc: 
            print("arndlc: ", arndlc)
            return jsonify({"Status": "A"}), 200

        try:
            if arndlcp:
                sns.unsubscribe(SubscriptionArn=arndlcp)
                print("Canceled the subscription.", end="\n\n")
            sns.subscribe(TopicArn=topicarn, Protocol="email", Endpoint=email)
        except Exception as e:
            print("An error occurred: ", str(e))
            return jsonify({"status": "error", "message": str(e)}), 500

        return jsonify({"Status": "F"})

@app.route("/dysend")
def d():
    if not request.headers.get("Referer"):
        abort(403)

    text = request.args.get("q")
    num = request.args.get("a")

    numbers = list("0123")
    symbs = ["🌞", "☁️", "🌧️", "🌨️"]

    numsymdict = dict(zip(numbers, symbs))
    sysel = numsymdict.get(num, "")

    textt = f"{text} {sysel}" if sysel else text

    try:
        
        dbtablename = dn.list_tables().get("TableNames")
        print("dbtablename: ", dbtablename)

        if not dbtablename:
            tablename = str(uuid.uuid4())

            print("config.js exists: ", os.path.exists("static/config.js"))
            with open("static/config.js", "r") as config:
                config.seek(0)
                configt = config.read()
                print(configt)

                try:
                    filenm = json.loads(configt)
                except Exception as e:
                    print("Error: ", str(e))
                    return jsonify({"status": "error", "message": str(e)}), 500

            dn.create_table(
                TableName=tablename,
                KeySchema=filenm["KeySchema"],
                AttributeDefinitions=filenm["AttributeDefinitions"],
                ProvisionedThroughput=filenm["ProvisionedThroughput"]
            )

            while True:
                tbon = dn.describe_table(TableName=tablename)
                if tbon["Table"]["TableStatus"] == "ACTIVE":
                    break
                print("Waiting for the table to be set...")
                sleep(5)


        email = session.get("email")
        topicarn = session.get("topicarn")


        dbtablename = dn.list_tables().get("TableNames")
        tablename = dbtablename[0]
        print(tablename, end="\n\n")



        dn.put_item(
            TableName=tablename,
            Item={
                "email": {"S": email},
                "trow": {"S": textt},
                "num": {"S": str(datetime.datetime.now())}
            },
        )
        


        itemsval = dn.scan(TableName=tablename).get("Items") 
        itemsval = dn.scan(TableName=tablename).get("Items") 
        itemsval = dn.scan(TableName=tablename).get("Items") 

        newitem= {'email': {'S': email}, 'trow': {'S': textt}, 'num': {'S': '2025-03-11 18:26:36.512188'}} 

        print(itemsval, end="\n\n")

        
        if itemsval:

            if len(itemsval) > 5:
                key = {
                    "email": itemsval[0]["email"],
                    "num": itemsval[0]["num"]
                }

                print("The last item is removing... ")
                print(key, end="\n\n")

                dn.delete_item(TableName=tablename, Key=key)


            itemsvalsf = [list(i.values())[1].get("S", 0) for i in itemsval if len(list(i.values())) >= 2]
            litemsvalsf = list(filter(lambda x: x, itemsvalsf))


    except Exception as e:
        print("An error occurred: ", str(e))
        return jsonify({"status": "error", "message": str(e)}), 500
 


    try:
        sns.publish(Subject="Message", Message=json.dumps(textt, ensure_ascii=False), TopicArn=topicarn)

    except Exception as e:
        print("An error occurred", str(e))
        print("Topicarn: ", topicarn, end="\n\n")
        return jsonify({"status": "error", "message": str(e)}), 500

    print("Item has been putted", end="\n\n")

    print(itemsval)

    return jsonify({"Items": litemsvalsf if itemsval else [textt]}), 200

if __name__ == "__main__":
    app.run(debug=True)

