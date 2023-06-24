"""

	{
	MessageType: "GetLastQuoteOptionGreeks",
	Exchange: "NFO",
	Tokens: [{"Value":"39489"},{"Value":"39487"},{"Value":"39487"},{"Value":"39487"},{"Value":"39487"}
	{"Value":"39489"},{"Value":"39487"},{"Value":"39487"},{"Value":"39487"},{"Value":"39487"}
	{"Value":"39489"},{"Value":"39487"},{"Value":"39487"},{"Value":"39487"},{"Value":"39487"}
	{"Value":"39489"},{"Value":"39487"},{"Value":"39487"},{"Value":"39487"},{"Value":"39487"}
	{"Value":"39489"},{"Value":"39487"},{"Value":"39487"},{"Value":"39487"},{"Value":"39487"}]
	};
	var message = JSON.stringify(request);
	websocket.send(message);

	{
	MessageType: "GetLastQuoteOptionGreeks",
	Exchange: "NFO",
	Tokens: [{"Value":"39489"},{"Value":"39487"},{"Value":"39487"},{"Value":"39487"},{"Value":"39487"}
	{"Value":"39489"},{"Value":"39487"},{"Value":"39487"},{"Value":"39487"},{"Value":"39487"}
	{"Value":"39489"},{"Value":"39487"},{"Value":"39487"},{"Value":"39487"},{"Value":"39487"}
	{"Value":"39489"},{"Value":"39487"},{"Value":"39487"},{"Value":"39487"},{"Value":"39487"}
	{"Value":"39489"},{"Value":"39487"},{"Value":"39487"},{"Value":"39487"},{"Value":"39487"}]
	};
	var message = JSON.stringify(request);
	websocket.send(message);

	{
	MessageType: "GetLastQuoteOptionGreeks",
	Exchange: "NFO",
	Tokens: [{"Value":"39489"},{"Value":"39487"},{"Value":"39487"},{"Value":"39487"},{"Value":"39487"}
	{"Value":"39489"},{"Value":"39487"},{"Value":"39487"},{"Value":"39487"},{"Value":"39487"}
	{"Value":"39489"},{"Value":"39487"},{"Value":"39487"},{"Value":"39487"},{"Value":"39487"}
	{"Value":"39489"},{"Value":"39487"},{"Value":"39487"},{"Value":"39487"},{"Value":"39487"}
	{"Value":"39489"},{"Value":"39487"},{"Value":"39487"},{"Value":"39487"},{"Value":"39487"}]
	};
	var message = JSON.stringify(request);
	websocket.send(message);

	{
	MessageType: "GetLastQuoteOptionGreeks",
	Exchange: "NFO",
	Tokens: [{"Value":"39489"},{"Value":"39487"},{"Value":"39487"},{"Value":"39487"},{"Value":"39487"}
	{"Value":"39489"},{"Value":"39487"},{"Value":"39487"},{"Value":"39487"},{"Value":"39487"}
	{"Value":"39489"},{"Value":"39487"},{"Value":"39487"},{"Value":"39487"},{"Value":"39487"}
	{"Value":"39489"},{"Value":"39487"},{"Value":"39487"},{"Value":"39487"},{"Value":"39487"}
	{"Value":"39489"},{"Value":"39487"},{"Value":"39487"},{"Value":"39487"},{"Value":"39487"}]
	};
	var message = JSON.stringify(request);
	websocket.send(message);

	{
	MessageType: "GetLastQuoteOptionGreeks",
	Exchange: "NFO",
	Tokens: [{"Value":"39489"},{"Value":"39487"},{"Value":"39487"},{"Value":"39487"},{"Value":"39487"}
	{"Value":"39489"},{"Value":"39487"},{"Value":"39487"},{"Value":"39487"},{"Value":"39487"}
	{"Value":"39489"},{"Value":"39487"},{"Value":"39487"},{"Value":"39487"},{"Value":"39487"}
	{"Value":"39489"},{"Value":"39487"},{"Value":"39487"},{"Value":"39487"},{"Value":"39487"}
	{"Value":"39489"},{"Value":"39487"},{"Value":"39487"},{"Value":"39487"},{"Value":"39487"}]
	};
	var message = JSON.stringify(request);
	websocket.send(message);

	{
	MessageType: "GetLastQuoteOptionGreeks",
	Exchange: "NFO",
	Tokens: [{"Value":"39489"},{"Value":"39487"},{"Value":"39487"},{"Value":"39487"},{"Value":"39487"}
	{"Value":"39489"},{"Value":"39487"},{"Value":"39487"},{"Value":"39487"},{"Value":"39487"}
	{"Value":"39489"},{"Value":"39487"},{"Value":"39487"},{"Value":"39487"},{"Value":"39487"}
	{"Value":"39489"},{"Value":"39487"},{"Value":"39487"},{"Value":"39487"},{"Value":"39487"}
	{"Value":"39489"},{"Value":"39487"},{"Value":"39487"},{"Value":"39487"},{"Value":"39487"}]
	};
	var message = JSON.stringify(request);
	websocket.send(message);


Exchange, Token(TokenNumber of Symbol), Timestamp, IV, Delta, Theta, Vega, Gamma, IVVwap, Vanna, Charm, Speed, Zomma, Color, Volga, Veta, ThetaGammaRatio, ThetaVegaRatio, DTR








"""

from import_files import *


def lastquoteoptiongreeks_store(tokens):
    lastquoteoptiongreeks = gw.lastquoteoptiongreeks.get(con, 'NFO', tokens)
    lastquoteoptiongreeks_response_str = json.loads(lastquoteoptiongreeks)

    if lastquoteoptiongreeks_response_str:
        print(lastquoteoptiongreeks_response_str)
        # Check if the data entry already exists
        existing_entry = lastquoteoptiongreeks_realtime_db.find_one(
            {'Exchange': lastquoteoptiongreeks_response_str['Exchange']})

        if existing_entry:
            data_id = existing_entry['_id']
            current_time = datetime.now()
            # Update existing entry with new data
            lastquoteoptiongreeks_response_str.update(
                {
                    'updated_at': current_time
                }
            )
            lastquoteoptiongreeks_historic_db.insert_one(lastquoteoptiongreeks_response_str)
            lastquoteoptiongreeks_realtime_db.update_one(
                {"_id": ObjectId(data_id),
                 'Exchange': lastquoteoptiongreeks_response_str['Exchange']
                 },
                {
                    '$set': {
                        "Token": lastquoteoptiongreeks_response_str['Token'],
                        'Timestamp': lastquoteoptiongreeks_response_str['Timestamp'],
                        'IV': lastquoteoptiongreeks_response_str['IV'],
                        'Delta': lastquoteoptiongreeks_response_str['Delta'],
                        'Theta': lastquoteoptiongreeks_response_str['Theta'],
                        'Vega': lastquoteoptiongreeks_response_str['Vega'],
                        'Gamma': lastquoteoptiongreeks_response_str['Gamma'],
                        'IVVwap': lastquoteoptiongreeks_response_str['IVVwap'],
                        'Vanna': lastquoteoptiongreeks_response_str['Vanna'],
                        'Charm': lastquoteoptiongreeks_response_str['Charm'],
                        'Speed': lastquoteoptiongreeks_response_str['Speed'],
                        'Zomma': lastquoteoptiongreeks_response_str['Zomma'],
                        'Color': lastquoteoptiongreeks_response_str['Color'],
                        'Volga': lastquoteoptiongreeks_response_str['Volga'],
                        'Veta': lastquoteoptiongreeks_response_str['Veta'],
                        'ThetaGammaRatio': lastquoteoptiongreeks_response_str['ThetaGammaRatio'],
                        'ThetaVegaRatio': lastquoteoptiongreeks_response_str['ThetaVegaRatio'],
                        'DTR': lastquoteoptiongreeks_response_str['DTR'],
                        'MessageType': lastquoteoptiongreeks_response_str['MessageType'],

                    }
                }
            )
            print("Existing data updated")

        else:
            current_time = datetime.now()
            lastquoteoptiongreeks_response_str.update(
                {
                    'created_at': current_time,
                    'updated_at': current_time
                }
            )
            lastquoteoptiongreeks_historic_db.insert_one(lastquoteoptiongreeks_response_str)
            lastquoteoptiongreeks_realtime_db.insert_one(lastquoteoptiongreeks_response_str)

        print("New data added")

    print("Waiting for 5 seconds")
    time.sleep(5)
    print("Wait over")


Tokens1 = [
    {"Value": "35656"},
    {"Value": "35657"},
    {"Value": "42744"},
    {"Value": "42751"},
    {"Value": "42765"},
    {"Value": "42768"},
    {"Value": "42769"},
    {"Value": "48024"},
    {"Value": "35657"},
    {"Value": "36705"},
    {"Value": "37435"},
    {"Value": "37436"},
    {"Value": "40760"},
    {"Value": "43152"},
    {"Value": "42843"},
    {"Value": "48072"},
    {"Value": "48077"},
    {"Value": "42107"},
    {"Value": "42165"},
    {"Value": "42191"},
    {"Value": "42195"},
    {"Value": "42197"},
    {"Value": "42931"},
    {"Value": "42201"},
    {"Value": "42213"},

]
Tokens2 = [
    {"Value": "42236"},
    {"Value": "42241"},
    {"Value": "42298"},
    {"Value": "42978"},
    {"Value": "42333"},
    {"Value": "43000"},
    {"Value": "48192"},
    {"Value": "42359"},
    {"Value": "42380"},
    {"Value": "45627"},
    {"Value": "46103"},
    {"Value": "43084"},
    {"Value": "46346"},
    {"Value": "51430"},
    {"Value": "51434"},
    {"Value": "43115"},
    {"Value": "51456"},
    {"Value": "43136"},
    {"Value": "48399"},
    {"Value": "51465"},
    {"Value": "51466"},
    {"Value": "51466"},
    {"Value": "51467"},
    {"Value": "51473"},
    {"Value": "51474"},
    {"Value": "51477"},
]

# for token in Tokens1:
#     lastquoteoptiongreeks_store(str(token['Value']))

# lastquoteoptiongreeks_store(Tokens)
# lastquoteoptiongreeks = gw.lastquoteoptiongreeks.get(con, 'NFO', Tokens)
# print(lastquoteoptiongreeks)
# lastquoteoptiongreeks = gw.lastquoteoptiongreeks.get(con, 'NFO', [{"Value": "42236"},
#     {"Value": "42241"},
#     {"Value": "42298"}])


while True:
    lastquoteoptiongreeks_store('48092')
