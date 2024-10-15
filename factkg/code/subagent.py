import openai
from openai import OpenAI
import sys
import os
from dotenv import load_dotenv

current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(os.path.dirname(current_dir))
sys.path.append(root_dir)
load_dotenv()

# GITIGNORE WHEN MAKING REPO PUBLIC
openai.api_key = os.getenv('OPENAI_KEY')

client = OpenAI(
    api_key = os.getenv('OPENAI_KEY')
)

sub_agent_2option = """
You are the evaluator. I will show you a claim and a triple set extracted from a graph. 
Based on the given triple set, let me know if it is possible to determine whether the claim is True or False. 
The triple set takes the form [head, relation, tail], which means 'Head's relation is tail.' 
If the relation starts with '~', it indicates a reverse relation, meaning 'Tail's relation is head.' 
The following cases may arise: Choose one option from 'Executable (True or False)' or 'Not executable(Insufficient evidence)'.
Refer to the explanations of the two options below to answer the Statement and Evaluation.

<Cases> 
1. If the triple sets are sufficient to determine the True/False of the claim --> Executable (True or False)
2. If the triple set is insufficient or ambiguos to determine the True/False of the claim --> Not executable (Insufficient evidence) 

<Example 1>
[User]
Claim : A fictional character, which was created by Joe Quesada, is broadcast on Lebanese Broadcasting Corporation and starred Tim Brooke-Taylor. 
Triple sets : [['Joe_Quesaa', '~creator', 'Azrael_(comics)'], ['Joe_Quesaa', '~creator', 'Menace_(Marvel_Comics)'], ['Joe_Quesaa', '~creator', 'Thomas_Logan'], ['Joe_Quesaa', '~creator', 'Carlie_Cooper']]
[ChatGPT]
Statement : It is impossible to determine the claim because information about the fictional character created by Joe Quesada being broadcast and starred cannot be found in the triple sets.
Evaluation : Not executable (Insufficient evidence)

<Example 2>
[User]
Claim : A soccer player's clubs are Esteghlal Ahvaz FC and also Al-Zawra'a SC which is managed by Basim Qasim. 
Triple sets: [["Al-Zawra'a_SC", 'manager', 'Basim_Qasim'], ['Esteghlal_Ahvaz_F.C.', 'manager', '"Siavash_Bakhtiarizadeh"'], ['Esteghlal_Ahvaz_F.C.', 'manager', 'Adnan_Hamad'], ['Basim_Qasim', 'managerclubs', 'Al_Shorta_SC'], ['Basim_Qasim', 'managerclubs', "Al-Zawra'a_SC"], ['Basim_Qasim', 'managerclubs', 'Duhok_SC'], ['Basim_Qasim', 'managerclubs', 'Zakho_FC'], ['Basim_Qasim', 'managerclubs', 'Sulaymaniya_FC'], ['Esteghlal_Ahvaz_F.C.', '~managerclubs', 'Ali_Firouzi'], ['Esteghlal_Ahvaz_F.C.', '~managerclubs', 'Gholam_Hossein_Mazloumi'], ['Esteghlal_Ahvaz_F.C.', '~managerclubs', 'Luka_Bonačić'], ['Esteghlal_Ahvaz_F.C.', '~managerclubs', 'Samad_Marfavi'], ['Esteghlal_Ahvaz_F.C.', '~managerclubs', 'Amir_Ghalenoei'], ['Esteghlal_Ahvaz_F.C.', '~managerclubs', 'Mehdi_Hasheminasab'], ['Esteghlal_Ahvaz_F.C.', '~managerclubs', 'Ali_Hanteh'], ['Esteghlal_Ahvaz_F.C.', '~managerclubs', 'Siavash_Bakhtiarizadeh'], ['Esteghlal_Ahvaz_F.C.', '~managerclubs', 'Mohammad_Ahmadzadeh'], ['Esteghlal_Ahvaz_F.C.', '~managerclubs', 'Mahmoud_Yavari'], ['Esteghlal_Ahvaz_F.C.', '~managerclubs', 'Bahram_Atef'], ['Esteghlal_Ahvaz_F.C.', '~managerclubs', 'Jalal_Cheraghpour'], ['Esteghlal_Ahvaz_F.C.', '~managerclubs', 'Akbar_Misaghian'], ['Esteghlal_Ahvaz_F.C.', '~managerclubs', 'Firouz_Karimi'], ['Esteghlal_Ahvaz_F.C.', '~managerclubs', 'Nasser_Hejazi'], ['Esteghlal_Ahvaz_F.C.', '~managerclubs', 'Majid_Jalali'], ['Esteghlal_Ahvaz_F.C.', '~managerclubs', 'Khodadad_Azizi'], ['Esteghlal_Ahvaz_F.C.', '~managerclubs', 'Davoud_Mahabadi']]
[ChatGPT]
Statement : It is clear that the manager of Al-Zawra'a SC is Basim Qasim, but with the given triples, it cannot be confirmed whether the player from Esteghlal Ahvaz FC is affiliated with Al-Zawra'a.
Evaluation : Not executable (Insufficient evidence)

<Example 3>
[User]
Claim : Tim Brooke-Taylor starred as a fictional character, which was first aired on 10/03/1983 and was broadcast by STV.
Triple sets : [[""1983-10-03"", '~firstAired', 'Terrahawks'], [""1983-10-03"", '~firstAired', 'Scarecrow_and_Mrs._King'], [""1983-10-03"", '~firstAired', 'Orm_and_Cheep'], [""1983-10-03"", '~firstAired', 'Watch_Mr._Wizard'], [""1983-10-03"", '~firstAired', 'Where_in_the_World_(UK_game_show)'], [""1983-10-03"", '~firstAired', 'Go_(game_show)'], ['"1983-10-03"', '~firstAired', 'Bananaman'], [""STV"", '~broadcastedBy', 'Bananaman'], [""STV"", '~channel', 'Brain_Box'], ['Tim_Brooke-Taylor', '~starring', 'How_to_Irritate_People'], ['Tim_Brooke-Taylor', '~starring', 'Broaden_Your_Mind'], ['Tim_Brooke-Taylor', '~starring', 'ISIRTA_songs'], ['Tim_Brooke-Taylor', '~starring', 'What_the_Dickens'], ['Tim_Brooke-Taylor', '~starring', 'Bananaman']]
[ChatGPT]
Statement : From the Evidence, we can know that there is the fictional character 'Bananaman' which satisfy all the information in the claim. 
Evaluation : Executable (True)


<Example 4>
[User]
Claim : Allama Iqbal International airport is located in Pakistan, the leader of the country is Gil Snider.
Triple sets : [['Allama_Iqbal_International_Airport', 'location', 'Punjab,_Pakistan'], ['Allama_Iqbal_International_Airport', 'location', 'Pakistan'], ['Allama_Iqbal_International_Airport', 'location', '"Punjab, Pakistan"'], ['Pakistan', 'leader', 'Anwar_Zaheer_Jamali'], ['Pakistan', 'leader', 'Mamnoon_Hussain'], ['Pakistan', 'leader', 'Nawaz_Sharif'], ['Pakistan', 'leader', 'Sardar_Ayaz_Sadiq'], ['"Gil Snider"', '~leaderName', 'Conroe,_Texas']]
[ChatGPT]
Statement : The 'Allama Iqbal International Airport' is located in 'Punjab, Pakistan', which confirms the first part of the claim. However, the leaders of Pakistan are 'Anwar Zaheer Jamali', 'Mamnoon Hussain', and 'Nawaz Sharif', among others, but 'Gil Snider' is not listed as a leader of Pakistan. Therefore, the second part of the claim is not supported.
Evaluation : Executable (False)


<Example 5>
[User]
Claim : Michele Marcolini played for Tokat Plevne Belediyesi and manages A.C. Lumezzane.
Triple sets : [['Michele_Marcolini', 'managerclubs', 'Real_Vicenza_V.S.'], ['Michele_Marcolini', 'managerclubs', 'A.C._Lumezzane'], ['Michele_Marcolini', 'currentclub', 'Real_Vicenza_V.S.'], ['A.C._Lumezzane', 'manager', 'Michele_Marcolini'], ['"Tokat Plevne Belediyesi"', '~clubs', 'Emre_Batur']]
[ChatGPT]
Statement : From the evidence, we can know that Michele_Marcolini manages A.C._Lumezzane, however there are no evidence that he played for Tokat Plevne Belediyesi. There for Michele_Marcolini is played for Tokat Plevne Belediyesi is not supported.
Evaluation : Executable (False)


<Example 6>
[User]
Claim : The city of Lahore is served by Allama Iqbal International airport, which is located in Pakistan and led by Mamnoon Hussain.
Triple sets : [['Allama_Iqbal_International_Airport', 'cityServed', 'Lahore'], ['Allama_Iqbal_International_Airport', 'operator', 'Pakistan_Civil_Aviation_Authority'], ['Lahore', '~cityServed', 'Allama_Iqbal_International_Airport'], ['Mamnoon_Hussain', '~president', 'Shahzada_Iftikhar_Uddin'], ['Mamnoon_Hussain', '~president', 'Yasin_Anwar'], ['Mamnoon_Hussain', '~president', 'Syed_Hassan_Raza'], ['Mamnoon_Hussain', '~president', 'Marvi_Memon'], ['Mamnoon_Hussain', '~president', 'Muhammad_Idrees_Khan_Safi'], ['Mamnoon_Hussain', '~president', 'Maliha_Lodhi'], ['Mamnoon_Hussain', '~president', 'Rana_Tanveer_Hussain'], ['Mamnoon_Hussain', '~president', 'Khawaja_Muhammad_Asif'], ['Mamnoon_Hussain', '~president', 'Muhammad_Atif_(politician)'], ['Mamnoon_Hussain', '~president', 'Baz_Muhammad_Khan'], ['Mamnoon_Hussain', '~president', 'Asif_Sandila'], ['Mamnoon_Hussain', '~president', 'Nawaz_Sharif'], ['Mamnoon_Hussain', '~president', 'Siraj-ul-Haq_Khan'], ['Mamnoon_Hussain', '~president', 'Rashad_Mahmood'], ['Mamnoon_Hussain', '~president', 'Saeeda_Iqbal'], ['Mamnoon_Hussain', '~president', 'Ghulam_Murtaza_Khan_Jatoi'], ['Mamnoon_Hussain', '~president', 'Agha_Rafiq_Ahmed_Khan'], ['Mamnoon_Hussain', '~president', 'Muhammad_Kazim_Khan'], ['Mamnoon_Hussain', '~president', 'Saira_Afzal_Tarar'], ['Mamnoon_Hussain', '~president', 'Zahid_Hamid'], ['Mamnoon_Hussain', '~president', 'Shah_Mehmood_Qureshi'], ['Mamnoon_Hussain', '~president', 'Muhammad_Daud_Khan_Achakzai'], ['Mamnoon_Hussain', '~president', 'Abdul_Haseeb_Khan'], ['Mamnoon_Hussain', '~president', 'Kamran_Michael'], ['Mamnoon_Hussain', '~president', 'Qamar_Zaman_Chaudhry'], ['Mamnoon_Hussain', '~president', 'Farah_Aqil'], ['Mamnoon_Hussain', '~president', 'Amir_Muqam'], ['Mamnoon_Hussain', '~president', 'Tahir_Rafique_Butt'], ['Mamnoon_Hussain', '~president', 'Sohail_Aman'], ['Mamnoon_Hussain', '~president', 'Anusha_Rahman'], ['Mamnoon_Hussain', '~president', 'Mehtab_Ahmed_Khan_Abbasi'], ['Mamnoon_Hussain', '~president', 'Zaheer-ul-Islam'], ['Mamnoon_Hussain', '~president', 'Rana_Muhammad_Iqbal_Khan_(politician)'], ['Mamnoon_Hussain', '~president', 'Sheikh_Aftab_Ahmed'], ['Mamnoon_Hussain', '~president', 'Tariq_Fatemi'], ['Mamnoon_Hussain', '~president', 'Syed_Mehdi_Shah'], ['Mamnoon_Hussain', '~president', 'Prince_Jam_Kamal_Khan'], ['Mamnoon_Hussain', '~president', 'Shehbaz_Sharif'], ['Mamnoon_Hussain', '~president', 'Jamshed_Dasti'], ['Mamnoon_Hussain', '~president', 'Muhammad_Baligh_Ur_Rehman'], ['Mamnoon_Hussain', '~president', 'Tahira_Asif'], ['Mamnoon_Hussain', '~president', 'Sanaullah_Zehri'], ['Mamnoon_Hussain', '~president', 'Hafiz_Hafeezur_Rehman'], ['Mamnoon_Hussain', '~president', 'Qaim_Ali_Shah'], ['Mamnoon_Hussain', '~president', 'Ishrat-ul-Ibad_Khan'], ['Mamnoon_Hussain', '~president', 'Kalsoom_Perveen'], ['Mamnoon_Hussain', '~president', 'Abdul_Nabi_Bangash'], ['Mamnoon_Hussain', '~president', 'Mohammad_Yousaf_(Pakistani_politician)'], ['Mamnoon_Hussain', '~president', 'Rai_Hassan_Nawaz'], ['Mamnoon_Hussain', '~president', 'Ahsan_Iqbal'], ['Mamnoon_Hussain', '~president', 'Shaukat_Ali_Yousafzai'], ['Mamnoon_Hussain', '~president', 'Ali_Amin_Khan'], ['Mamnoon_Hussain', '~president', 'Khawaja_Saad_Rafique'], ['Mamnoon_Hussain', '~president', 'Heman_Dass'], ['Mamnoon_Hussain', '~president', 'Raheel_Sharif'], ['Mamnoon_Hussain', '~president', 'Malik_Muhammad_Rafique_Rajwana'], ['Mamnoon_Hussain', '~president', 'Pervez_Khattak'], ['Mamnoon_Hussain', '~president', 'Shahid_Khaqan_Abbasi'], ['Mamnoon_Hussain', '~president', 'Jehangir_Bader'], ['Mamnoon_Hussain', '~president', 'Muhammad_Saleh_Shah'], ['Mamnoon_Hussain', '~president', 'Abdul_Qadir_Baloch'], ['Mamnoon_Hussain', '~president', 'Pir_Sadaruddin_Shah'], ['Mamnoon_Hussain', '~president', 'Abbas_Khan_Afridi'], ['Mamnoon_Hussain', '~president', 'Abdul_Hakeem_Baloch'], ['Mamnoon_Hussain', '~president', 'Ashtar_Ausaf_Ali'], ['Mamnoon_Hussain', '~president', 'Haji_Ghulam_Ali'], ['Mamnoon_Hussain', '~president', 'Khurram_Dastgir_Khan'], ['Mamnoon_Hussain', '~president', 'Malik_Rashid_Ahmed_Khan'], ['Mamnoon_Hussain', '~president', 'Shirala_Mallick'], ['Mamnoon_Hussain', '~president', 'Nasir-ul-Mulk'], ['Mamnoon_Hussain', '~president', 'Mir_Muhammad_Ali_Rind'], ['Mamnoon_Hussain', '~president', 'Chaudhry_Muhammad_Barjees_Tahir'], ['Mamnoon_Hussain', '~president', 'Sardar_Fateh_Muhammad_Muhammad_Hassani'], ['Mamnoon_Hussain', '~president', 'Sajid_Mir'], ['Mamnoon_Hussain', '~president', 'Ashfaq_Parvez_Kayani'], ['Mamnoon_Hussain', '~president', 'Usman_Ibrahim'], ['Mamnoon_Hussain', '~president', 'Pervez_Rashid'], ['Mamnoon_Hussain', '~president', 'Abdul_Malik_Baloch'], ['Mamnoon_Hussain', '~president', 'Rizwan_Akhtar'], ['Mamnoon_Hussain', '~president', 'Zahid_Khan'], ['Mamnoon_Hussain', '~president', 'Kamil_Ali_Agha'], ['Mamnoon_Hussain', '~president', 'Hafiz_Hamdullah'], ['Mamnoon_Hussain', '~president', 'Muhammad_Rafiq_Tarar']]
[ChatGPT]
Statement : Among the triple sets related to Mamnoon Hussain, there is an entity connected as 'president', but there is no direct triple indicating that he is the leader of Pakistan. The relation 'president' does not directly mean 'leader', so more definitive evidence is needed.
Evaluation : Not executable (Insufficient evidence)


<Example 7>
[User]
Claim : A food is part of Colombian cuisine, one of its ingredients is another food, that is found in the Andalusia region.
Triple sets : [['Colombian_cuisine', '~foodType', 'Pueblito_Viejo'], ['Andalusia', '~location', 'Sierra_de_la_Alfaguara'], ['Andalusia', '~location', 'Sierra_de_Los_Filabres'], ['Andalusia', '~location', 'Open_de_Andalucía'], ['Andalusia', '~location', 'Sierra_de_Cogollos'], ['Andalusia', '~location', 'Carteia'], ['Andalusia', '~location', '2012–13_Getafe_CF_season'], ['Andalusia', '~location', 'Bombing_of_Jaén'], ['Andalusia', '~location', 'Cabo_de_Gata-Níjar_Natural_Park'], ['Andalusia', '~location', 'CB_Sevilla'], ['Andalusia', '~location', 'Sierra_Norte_de_Sevilla'], ['Andalusia', '~location', 'Sierra_de_Aracena'], ['Andalusia', '~location', 'Pico_Mágina'], ['Andalusia', '~location', 'Bahía_de_Cádiz_Natural_Park'], ['Andalusia', '~location', 'Alcazaba_(Sierra_Nevada)'], ['Andalusia', '~location', 'Mosque–Cathedral_of_Córdoba'], ['Andalusia', '~location', '2004–05_Real_Madrid_C.F._season'], ['Andalusia', '~location', 'La_Maroma'], ['Andalusia', '~location', 'CB_Villa_de_Los_Barrios'], ['Andalusia', '~location', 'Alcazaba_of_Almería'], ['Andalusia', '~location', 'Ciudad_Deportiva_Rafael_Gómez'], ['Andalusia', '~location', 'Hotel_París_(Huelva)'], ['Andalusia', '~location', '2012–13_Recreativo_de_Huelva_season'], ['Andalusia', '~location', 'Sierra_Arana'], ['Andalusia', '~location', 'Sierra_de_Cazorla'], ['Andalusia', '~location', 'Despeñaperros'], ['Andalusia', '~location', 'CB_Ciudad_de_Huelva'], ['Andalusia', '~location', 'Seville_Cathedral'], ['Andalusia', '~location', 'Jabalcón'], ['Andalusia', '~location', 'Hotel_Anglo-Hispano'], ['Andalusia', '~location', 'Monastery_of_Santa_Maria_de_las_Cuevas'], ['Andalusia', '~location', '2014–15_CA_Osasuna_season'], ['Andalusia', '~location', 'La_Cala_Resort'], ['Andalusia', '~location', 'Palacio_de_Campo_Real'], ['Andalusia', '~location', 'Los_Millares'], ['Andalusia', '~location', '2014–15_Granada_CF_season'], ['Andalusia', '~location', 'Baloncesto_Málaga'], ['Andalusia', '~location', 'PS10_solar_power_plant'], ['Andalusia', '~location', 'IRAM_30m_telescope'], ['Andalusia', '~location', 'Sierra_de_Huétor'], ['Andalusia', '~location', 'Generalife'], ['Andalusia', '~location', 'Ciudad_Deportiva_José_Ramón_Cisneros_Palacios'], ['Andalusia', '~location', '2011_Volvo_World_Match_Play_Championship'], ['Andalusia', '~location', 'Montes_de_Málaga'], ['Andalusia', '~location', 'Ciudad_Deportiva_del_Granada_CF'], ['Andalusia', '~location', 'Los_Alcornocales_Natural_Park'], ['Andalusia', '~location', '2009_Volvo_World_Match_Play_Championship'], ['Andalusia', '~location', 'Sierra_Blanca_(Andalusia)'], ['Andalusia', '~location', 'Ciudad_Deportiva_de_El_Viso'], ['Andalusia', '~location', 'Sea_Life_Benalmádena'], ['Andalusia', '~location', '2013–14_CA_Osasuna_season'], ['Andalusia', '~location', 'El_Fraile_(Sierra_del_Cabo_de_Gata)'], ['Andalusia', '~location', 'Sierra_de_las_Nieves'], ['Andalusia', '~location', '2011–12_RCD_Mallorca_season'], ['Andalusia', '~location', 'Hotel_Pez_Espada'], ['Andalusia', '~location', 'Ramón_Sánchez_Pizjuán_Stadium'], ['Andalusia', '~location', 'Veleta_(Sierra_Nevada)'], ['Andalusia', '~location', 'Penibaetic_System'], ['Andalusia', '~location', 'CB_Granada'], ['Andalusia', '~location', '2014–15_Middlesbrough_F.C._season'], ['Andalusia', '~location', '2012_Volvo_World_Match_Play_Championship'], ['Andalusia', '~location', '2001–02_Real_Madrid_C.F._season'], ['Andalusia', '~location', 'Circuito_de_Jerez'], ['Andalusia', '~location', 'Sierra_de_Baza'], ['Andalusia', '~location', 'CB_Ciudad_de_Algeciras'], ['Andalusia', '~location', 'Baelo_Claudia'], ['Andalusia', '~location', 'Subbaetic_System'], ['Andalusia', '~location', 'Museum_of_Almería'], ['Andalusia', '~location', 'General_Archive_of_the_Indies'], ['Andalusia', '~location', 'Ciudad_Deportiva_Luis_del_Sol'], ['Andalusia', '~location', 'Peña_de_los_Enamorados'], ['Andalusia', '~location', 'Caminito_del_Rey'], ['Andalusia', '~location', 'Sierra_Sur_de_Jaén'], ['Andalusia', '~location', 'CD_Huelva_Baloncesto'], ['Andalusia', '~location', 'San_Roque_Club'], ['Andalusia', '~location', 'CD_Oximesa'], ['Andalusia', '~location', 'CB_Morón'], ['Andalusia', '~location', 'Pico_del_Caballo'], ['Andalusia', '~location', 'Sierra_de_Mijas'], ['Andalusia', '~location', '2012–13_RCD_Espanyol_season'], ['Pueblito_Viejo', 'foodType', 'Colombian_cuisine']]
[ChatGPT]
Statement : The evidence supporting that Pueblito Viejo’s food type is Colombian cuisine is clear, but there is a lack of information about the ingredients.
Evaluation : Not executable (Insufficient evidence)


<Example 8>
[User]
Claim : The asteroid 1147 Stavropolis discovered on the 11th of June 1929 with a rotation period of 20378.5 has apoapsis of 418476000000.0.
Triple sets :[['"1929-06-11"', '~discovered', '1147_Stavropolis'], ['1147_Stavropolis', 'discovery', '"yes"'], ['1147_Stavropolis', 'rotation', '"20376.0"'], ['"20378.5"', '~rotationPeriod', '1147_Stavropolis'], ['1147_Stavropolis', 'apoapsis', '"418476000000.0"']]
[ChatGPT]
Statement : The apoapsis of '1147_Stavropolis' is confirmed as '"418476000000.0"', which matches the claim. Therefore, the claim is True.
Evaluation : Executable (True)


<Example 9>
[User]
Claim : The icebreaker Aleksey Chirikov was built by a country's (led by Juha Sipila) Arctech Helsinki Shipyard.
Triple sets : [['Arctech_Helsinki_Shipyard', '~shipBuilder', 'NB_510_(icebreaker)'], ['Arctech_Helsinki_Shipyard', '~shipBuilder', 'Aleksey_Chirikov_(icebreaker)'], ['Arctech_Helsinki_Shipyard', '~shipBuilder', 'Vitus_Bering_(icebreaker)'], ['Arctech_Helsinki_Shipyard', 'locationCity', 'Helsinki'], ['Juha_Sipilä', 'office', '"Leader of the Centre Party"'], ['Juha_Sipilä', 'office', '"44"'], ['Juha_Sipilä', 'predecessor', 'Alexander_Stubb'], ['Juha_Sipilä', 'predecessor', 'Mari_Kiviniemi'], ['Juha_Sipilä', '~governmentHead', 'Sipilä_Cabinet'], ['Juha_Sipilä', 'title', 'Speaker_of_the_Parliament_of_Finland'], ['Juha_Sipilä', 'title', '"Leader of the Centre Party"'], ['Juha_Sipilä', 'title', 'Prime_Minister_of_Finland']]
[ChatGPT]
Statement : The exploration reveals that Juha Sipilä holds the title of "Prime Minister of Finland", indicating that he is associated with Finland. Now, I can verify the claim that the icebreaker Aleksey Chirikov was built by Arctech Helsinki Shipyard, which is in Finland, under the leadership of Juha Sipilä.
Evaluation : Executable (True)




Now, it's your turn. Continue your 'Statement and Evaluation' task. Response must have same form with upper examples.
[User]
Claim : <<<<CLAIM>>>>
Triple set : <<<<Triple set>>>>
"""


def feedback(claim, gold_set, f):
    
    engine="gpt-3.5-turbo-0125"
    #engine = "gpt-4o-mini-2024-07-18"

    sub_response = None
    
    f.write(f"\nGOLD SET!!!!!!!!!!!!!!!!!!!!!!\n{gold_set}")    
    
    conversation = [{"role": "system", "content": "You are a helpful assistant."}]
    prompt = sub_agent_2option.replace('<<<<CLAIM>>>>', claim).replace('<<<<Triple set>>>>', str(gold_set))
    conversation.append({"role": "user", "content": prompt})
    
    for i in range(5):

        
        try :  
            response = client.chat.completions.create( model=engine, messages=conversation, temperature= 0.3, top_p = 0.1)
            assistant_response = response.choices[0].message.content.strip()
            #print(assistant_response)
            try:
                sub_statement = assistant_response.split("Statement : ")[1].split("Evaluation")[0].strip()
                sub_result = assistant_response.split("Evaluation")[1].strip()
                
                
                if "(Insufficient evidence)" in sub_result:
                    #sub_response = "We don't have enough evidence to verify the claim. You must extract more information from the graph data."
                    sub_response = sub_statement
                    case =1
                    prediction = None
                    break
                elif "(Complex claim)" in sub_result:
                    sub_response = "Done!! Abstain"
                    case=2
                    prediction = "Abstain"
                    break
                else: 
                    #Executable case
                    if 'True' in sub_result or 'true' in sub_result:
                        sub_response = "Done!! True"
                        prediction = 'True'
                    else:
                        sub_response = "Done!! False"
                        prediction = 'False'
                    case=3
                    break
            except:
                continue

        

        except openai.APIError as e:
                #Handle API error here, e.g. retry or log
                print(f"OpenAI API returned an API Error: {e}")
                continue
    
    # Ensure sub_response has a value before returning
    if sub_response is None:
        sub_response = "There is problem in server. Please call Verification[] one more time/"
        case = -1
        prediction = None
    
    
    return sub_response, case, prediction