import pymysql, time, random
from geopy.distance import geodesic
from colorama import Fore, Style

# Globaalit muuttujat:

user_information = {
    'login': '',
    'user_name': '',
    'user_password': '',
    'balance': 0,
    'current_airport': '',
    'current_country': '',
    'current_continent': '',
    'current_icao_code': '',
    'visited_countries': 0,
    'distance_traveled': 0,
}

connection = pymysql.connect(
    host='localhost',
    port=3306,
    database='airplane_simulator_v3',
    user='user',
    password='password',
    autocommit=True,
)


# Yksittäisfunktiot:

# Testattu
def feedback():
    while True:
        if user_information['user_name']:
            print(Style.BRIGHT, Fore.LIGHTRED_EX)
            feedback = str(input(
                "Anna palaute tai kehitysehdotus pelistä (minimi sana määrä 10) tai poistu kirjoittamalla 'back'(EI VALMIS, KIRJOITA 'BACK'): ").lower())

            if len(feedback.split()) >= 10:
                feedback_sensor(feedback)
                fb = 'Palaute tallennettu onnistuneesti.'
                break
            elif feedback == 'back':
                fb = 'Palautetta ei lähetetty.'
                break
            elif len(feedback.split()) < 10:
                print("Haluamme järkevää palautetta, jonka takia sanamäärä on asetettu 10:neen.")
                continue
            else:
                print("Tarkista syöte.")
        else:
            fb = 'Sinun pitää olla kirjautuneena käyttäjälle antaaksesi palautetta.'
            break
    user_information.update({'login': ''})
    return fb


# Testattu
def feedback_sensor(feedback):
    pass
    # Tähän tulis lähetys ja tallennus tietokannan feedback-osioon.


# Testattu
def update_user_info(user_info):
    try:
        # Tietokannasta haetun tiedon tallennus sanakirjaan:
        user_information.update({'login': True})
        user_information.update({'user_name': user_info[0]})
        user_information.update({'user_password': user_info[1]})
        user_information.update({'current_airport': user_info[2]})
        user_information.update({'current_country': user_info[3]})
        user_information.update({'current_continent': user_info[4]})
        user_information.update({'current_icao_code': user_info[5]})
        user_information.update({'visited_countries': user_info[6]})
        user_information.update({'distance_traveled': user_info[7]})
        user_information.update({'balance': user_info[8]})
        palaute = ' Käyttäjätiedot tallennettu onnistuneesti.'

    except:
        # Odottamaton virhe
        palaute = 'Tallennus epäonnistui.'

    finally:
        return palaute

    # Testattu - Tallentaa tiedot automaattisesti ja kirjautuu ulos käyttäjältä.


# Kirjaa käyttäjän ulos ja tallentaa automaattisesti datan tietokantaan.
def logoff():
    while True:
        if user_information['user_name']:
            print(Style.BRIGHT, Fore.LIGHTRED_EX)
            logoff = print(
                "Paina [ENTER] kirjautuaksesi ulos. Peli tallentaa edistymisen automaattisesti.\n(2) Kirjoita 'back' palataksesi peliin.")
            logoff = str(input("[ENTER] tai 'back': ").lower())

            if logoff == '':
                save_data()
                user_information.update({'login': ''})
                user_information.update({'user_name': ''})
                user_information.update({'user_password': ''})
                user_information.update({'balance': 0})
                user_information.update({'current_airport': ''})
                user_information.update({'current_country': ''})
                user_information.update({'current_continent': ''})
                user_information.update({'current_icao_code': ''})
                user_information.update({'visited_countries': 0})
                user_information.update({'distance_traveled': 0})
                log = 'menu'
                break

            elif logoff == 'back':
                log = 'back'
                break
            else:
                print("Tarkista syöte.")
                continue

        elif user_information['login'] == False:
            break

        else:
            print(Style.BRIGHT, Fore.LIGHTRED_EX)
            print("Et ole kirjautunut sisään.")
            while True:
                enter = input("Paina [ENTER] palataksesi -->").lower()
                if enter == '':
                    user_information.update({'login': False})
                    log = 'menu'
                    break
                else:
                    print("Tarkista syöte.")
                    continue

    user_information.update({'login': ''})
    return log


# Testattu - Tallentaa tiedot automaattisesti
def save_data():
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT password FROM game WHERE nick = %s;", (user_information['user_name']))
            userdata = cursor.fetchone()

            if userdata:
                # Päivitetään tietokannasta jo löytyvä käyttäjä:
                updatesql = """
                UPDATE game 
                SET balance =  %s, 
                    current_airport = %s, 
                    current_country = %s, 
                    visited_countries =  %s, 
                    current_continent = %s, 
                    distance_km =  %s,
                    current_icao_code = %s 
                WHERE nick = %s;
                """
                cursor.execute(updatesql, (
                    user_information['balance'],
                    user_information['current_airport'],
                    user_information['current_country'],
                    user_information['visited_countries'],
                    user_information['current_continent'],
                    user_information['distance_traveled'],
                    user_information['current_icao_code'],
                    user_information['user_name']
                ))
                print("Käyttäjätiedot päivitettiin onnistuneesti.")

            else:
                # Lisätään uusi käyttäjä
                insertsql = """
                INSERT INTO game (nick, password, balance, current_airport, current_country, current_icao_code, current_continent, visited_countries, distance_km) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
                """
                cursor.execute(insertsql, (
                    user_information['user_name'],
                    user_information['user_password'],
                    user_information['balance'],
                    user_information['current_airport'],
                    user_information['current_country'],
                    user_information['current_icao_code'],
                    user_information['current_continent'],
                    user_information['visited_countries'],
                    user_information['distance_traveled']
                ))
                print("Uuden käyttäjän tiedot tallennettiin onnistuneesti.")

    except pymysql.MySQLError as e:
        print(f"Tietokantavirhe: {e}")
    except Exception as e:
        print(f"Satunnaisvirhe: {e}")

    finally:
        # Nollataan numero arvot, jotta käyttäjä ei voi kasvattaa näitä pelaamatta.
        user_information.update({'balance': 0})
        user_information.update({'distance_traveled': 0})
        user_information.update({'visited_countries': 0})


# Testattu - Nollaa käyttäjätiedot niin, että voiton tai häviön jälkeen käyttäjän on mahdollista aloittaa uusi peli samalla käyttäjällä.
def nollaaja():
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT password FROM game WHERE nick = %s;", (user_information['user_name']))
            userdata = cursor.fetchone()

            if userdata:
                # Päivitetään tietokannasta jo löytyvä käyttäjä:
                updatesql = """
                UPDATE game 
                SET balance =  %s, 
                    current_airport = %s, 
                    current_country = %s, 
                    visited_countries =  %s, 
                    current_continent = %s, 
                    distance_km =  %s,
                    current_icao_code = %s 
                WHERE nick = %s;
                """
                cursor.execute(updatesql, (
                    0,
                    user_information['current_airport'],
                    user_information['current_country'],
                    0,
                    user_information['current_continent'],
                    0,
                    user_information['current_icao_code'],
                    user_information['user_name']
                ))
                print("Käyttäjätiedot päivitettiin onnistuneesti.")


    except pymysql.MySQLError as e:
        print(f"Tietokantavirhe: {e}")
    except Exception as e:
        print(f"Satunnaisvirhe: {e}")

    finally:
        # Nollataan numero arvot, jotta käyttäjä ei voi kasvattaa näitä pelaamatta.
        user_information.update({'balance': 0})
        user_information.update({'distance_traveled': 0})
        user_information.update({'visited_countries': 0})


# Testattu - Hakee päivitetyt käyttäjätiedot 1. save_data() --> 2. fetch_user_statistics
def fetch_user_statistics():
    try:

        with connection.cursor() as cursor:
            infosql = "SELECT balance, current_airport, current_country, current_icao_code, current_continent, visited_countries, distance_km FROM game WHERE nick = %s;"
            cursor.execute(infosql, (user_information['user_name']))
            data = cursor.fetchone()

            if cursor.rowcount:
                user_data = f"User balance: [{data[0]}]\nCurrent airport: [{data[1]}]\nCurrent country: [{data[2]}]\nCurrent ICAO-code: [{data[3]}]\nCurrent continent: [{data[4]}]\nVisited countries: [{data[5]}]\nTraveled kilometers: [{data[6]}]"
            else:
                user_data = 'Tietokantavirhe: Käyttäjätieto ei ole tallentunut tietokantaan.'
    except pymysql.MySQLError as e:
        user_data = f"Tietokantavirhe: {e}"
    except Exception as e:
        user_data = f"Odottamaton virhe: {e}"
    finally:
        return user_data


# Testattu - Hakee vanhan pelin tietokannasta, pelin jatkaminen mahdollista tämän jälkeen aloitusvalikon 'Aloita'-painikkeesta.
def continue_game():
    while True:
        if user_information['login'] == True or user_information['login'] == False:
            break

        else:
            print(Style.BRIGHT, Fore.LIGHTRED_EX + "Hae käyttäjänimeä tai mene takaisin kirjoittamalla 'Menu'")
            name = str(input(" ['Käyttäjänimi' tai 'Menu']: "))
            if name == 'Menu' or name == 'menu':
                user_information.update({'login': False})
                break

            elif 20 >= len(name) >= 1:
                namesql = "SELECT nick, password, current_airport, current_country, current_continent, current_icao_code, visited_countries, distance_km, balance FROM game WHERE nick = %s;"
                with connection.cursor() as cursor:
                    cursor.execute(namesql, (name))
                    user_info = cursor.fetchone()

                    if user_info:
                        print(f" Käyttäjä nimellä {user_info[0]} löydettiin.")
                        while True:
                            if user_information['login'] == True or user_information['login'] == False:
                                break
                            else:
                                print(" (I) Kirjaudu sisään kirjoittamalla 'Kirjaudu'.")
                                print(" (II) Poistu kirjoittamalla 'Menu'.")
                                login = input(" ['Kirjaudu' tai 'Menu']: ").lower()
                                if login == 'kirjaudu':
                                    while True:
                                        userpwd = str(input(" Anna käyttäjän salasana: "))
                                        if userpwd == user_info[1]:
                                            user_data_changed = update_user_info(user_info)
                                            print(user_data_changed)
                                            break
                                        else:
                                            print(" Tarkista syöte.")
                                            continue

                                elif login == 'menu':
                                    user_information.update({'login': False})
                                    break
                                else:
                                    print(" Tarkista syöte.")
                                    continue
                    else:
                        print(f" Nimellä {name} ei löytynyt käyttäjää.")
                        while True:
                            print(" (I) Yritä toista nimeä kirjoittamalla 'Kirjaudu'.")
                            print(" (II) Poistu kirjoittamalla 'Menu'.")
                            login = input(" ['Kirjaudu' tai 'Menu']: ").lower()
                            if login == 'kirjaudu':
                                break
                            elif login == 'menu':
                                user_information.update({'login': False})
                                break
                            else:
                                print(' Tarkista syöte.')
                                continue
            else:
                print(" Haettava nimi on oltava pituudeltaan 1-20 merkkiä.")
                continue
    return user_information['login']


# Testattu 2 - Tarkistaa jos pelaaja häviää tai voittaa pelin, eli jos pelaajan rahamäärä on $0 tai voittaessa yli $100 000.
def check_player_status():
    user_data = fetch_user_statistics()  # Hakee uusimmat tiedot tietokannasta

    if not user_data:
        print("Käyttäjätietoja ei löytynyt.")
        return

    # Tarkista, että user_data sisältää "User balance:"-rivin
    if "User balance:" not in user_data:
        print("Virhe: Käyttäjätiedoista puuttuu saldo.")
        return

    try:
        # Etsi 'balance'-rivi ja jäsennä se
        balance_line = [line for line in user_data.split('\n') if line.startswith("User balance:")][0]
        balance_str = balance_line.split(': ')[1]  # Poimi saldon arvo (esim. "[121773]")

        # Poista hakasulkeet ja muunna kokonaisluvuksi
        balance_str = balance_str.replace('[', '').replace(']', '')  # Poista hakasulkeet
        balance = int(balance_str)  # Muunna kokonaisluvuksi

        entire_balance = balance + user_information['balance']

        if entire_balance >= 100000:
            print(Style.BRIGHT, Fore.LIGHTRED_EX)
            print("Onneksi olkoon! Olet voittanut pelin!")
            show_endstats()

        elif entire_balance <= 0:
            print(Style.BRIGHT, Fore.LIGHTRED_EX)
            print("Valitettavasti hävisit pelin. Rahasi loppuivat.")
            show_endstats()

    except (IndexError, ValueError) as e:
        print(f"Virhe: Saldoa ei voitu jäsentää. Virheen tiedot: {e}")


# Testattu - Pelin päätyttyä näyttää kertaalleen vielä lopetus statistiikan.
def show_endstats():
    with connection.cursor() as cursor:
        cursor.execute(
            f"SELECT balance, current_airport, current_country, current_continent, visited_countries, distance_km FROM game WHERE nick = '{user_information['user_name']}';")
        result = cursor.fetchone()
        if result:
            print("\nLopulliset tilastosi:")
            print(f"Käyttäjänimi: {user_information['user_name']}")
            print(f"Saldo: ${result[0]}")
            print(f"Nykyinen lentokenttä: {result[1]}")
            print(f"Nykyinen maa: {result[2]}")
            print(f"Nykyinen maanosa: {result[3]}")
            print(f"Vierailtujen maiden määrä: {result[4]}")
            print(f"Matkustetut kilometrit: {result[5]}")


# Testattu
def show_endstats():
    with connection.cursor() as cursor:
        cursor.execute(
            f"SELECT balance, current_airport, current_country, current_continent, visited_countries, distance_km FROM game WHERE nick = '{user_information['user_name']}';")
        result = cursor.fetchone()
        if result:
            print("\nLopulliset tilastosi:")
            print(f"Käyttäjänimi: {user_information['user_name']}")
            print(f"Saldo: ${result[0]}")
            print(f"Nykyinen lentokenttä: {result[1]}")
            print(f"Nykyinen maa: {result[2]}")
            print(f"Nykyinen maanosa: {result[3]}")
            print(f"Vierailtujen maiden määrä: {result[4]}")
            print(f"Matkustetut kilometrit: {result[5]}")


# Pelin generoivat funktiot:

# Testattu - Pelin aloitusvalikko (Aloita, jatka, palaute, profiili, kirjaudu ulos)
def prequestion():
    print('')
    print('')
    underlined = "           " + "\u0332".join("LentoKoneSimuLaattori ")
    print(Style.BRIGHT, Fore.LIGHTRED_EX + underlined)
    print(Style.BRIGHT, Fore.LIGHTGREEN_EX)
    print('---------------------------------------------------')
    print("       Tervetuloa lentokone simulaattoriin!            ")
    print(
        "       Pelin ideasta pääset helpoiten perille        \n       aloittamalla pelin ja seuraamalla ohjeita\n       ainakin ekoilla peli kerroilla.")
    print('---------------------------------------------------')

    while True:
        print(Style.BRIGHT, Fore.LIGHTGREEN_EX)
        if len(user_information['user_password']) == 0:
            print("(I)   Aloita uusi peli kirjoittamalla 'Aloita'.")
            print("(II)  Jatka peliä kirjoittamalla 'Jatka'.")
            print("(III) Anna palautetta/ehdotuksia kirjoittamalla 'Palaute'.")
            print("(IV)  Tarkista käyttäjätietosi kirjoittamalla 'Profiili'.")
            print("(V)   Kirjaudu ulos kirjoittamalla 'Ulos'.")
            print("(VI)  Nollaa kaikki tiedot 'Nollaa'.")

        else:
            print("(I)   Jatka peliä kirjoittamalla 'Aloita'.")
            print("(II)  Kirjaudu sisään toiselle käyttäjälle kirjoittamalla 'Jatka'.")
            print("(III) Anna palautetta/ehdotuksia kirjoittamalla 'Palaute'.")
            print("(IV)  Tarkista käyttäjätietosi kirjoittamalla 'Profiili'.")
            print("(V)   Kirjaudu ulos kirjoittamalla 'Ulos'.")
            print("(VI)  Nollaa kaikki tiedot 'Nollaa'.")

        start = input("['Aloita' 'Jatka' 'Palaute' 'Profiili' 'Kirjaudu ulos' 'Nollaa']: ").lower()
        if start == 'aloita':
            break

        elif start == "jatka":
            start = continue_game()
            if start == False:
                user_information.update({'login': ''})
                continue
            else:
                user_information.update({'login': ''})
                continue
        elif start == 'palaute':
            palaute = feedback()
            print(Style.BRIGHT, Fore.LIGHTRED_EX)
            print(palaute)
            enter = input("Paina [ENTER] palataksesi -->").lower()
            if enter == '':
                continue
        elif start == 'profiili':
            data = fetch_user_statistics()
            print(Style.BRIGHT, Fore.LIGHTRED_EX)
            if user_information['user_name']:
                data = fetch_user_statistics()
                print(f"Käyttäjän [{user_information['user_name']}] Tiedot\n" + data)
                enter = input("Paina [ENTER] palataksesi -->").lower()
                if enter == '':
                    continue

                else:
                    print('Tarkista syöte.')
            else:
                print("Et ole kirjautunut sisään.")
                while True:
                    enter = input("Paina [ENTER] palataksesi -->").lower()
                    if enter == '':
                        break
                    else:
                        print("Tarkista syöte.")
                        continue
        elif start == 'ulos':
            menu_or_game = logoff()
            if menu_or_game:
                continue

        elif start == 'nollaa':
            print(Style.BRIGHT, Fore.LIGHTRED_EX)
            if user_information['user_name']:
                nollaaja()
                data = fetch_user_statistics()
                print(f"Käyttäjän [{user_information['user_name']}] Tiedot\n" + data)
                enter = input("Paina [ENTER] palataksesi -->").lower()
                if enter == '':
                    continue

                else:
                    print('Tarkista syöte.')
            else:
                print("Et ole kirjautunut sisään.")
                while True:
                    enter = input("Paina [ENTER] palataksesi -->").lower()
                    if enter == '':
                        break
                    else:
                        print("Tarkista syöte.")
                        continue
        else:
            print("Tarkista syöte.")
            continue
    return start


# Testattu - Peliä määrittävä funktio, uusi vai vanha peli.
def gamestart():
    if len(user_information['user_password']) == 0 or user_information['login'] == '':
        gamestarts = prequestion()
        if gamestarts == 'aloita':
            newstart()

        # Testattu - Poistaa tietokannasta duplikaatit


def namecheck(x):
    try:  # Tarkistaa jos tietokannasta löytyy jo käyttäjä, jotta vältetään saman käyttäjän päivitys, vaikka kyseessä on eri pelaaja.
        with connection.cursor() as cursor:
            checkingsql = "SELECT nick from game where nick = %s"
            cursor.execute(checkingsql, (x))
            data = cursor.fetchone()

            if data:
                feed = 'Used'
            else:
                feed = 'Free'
    except pymysql.MySQLError as e:
        print(f"Tietokantavirhe: {e}")
    except Exception as e:
        print(f"Satunnaisvirhe: {e}")

    finally:
        return feed


# Testattu - Uuden käyttäjän nimen ja salasanan hakeminen
def newstart():
    while True:
        if len(user_information['user_name']) > 0:
            break
        elif len(user_information['user_password']) == 0 or user_information['user_password'] == 'reset':
            print(Style.BRIGHT, Fore.LIGHTRED_EX)
            name = str(input("Aloita valitsemalla itsellesi käyttäjänimi: "))
            user_information.update({'user_password': ''})
            if 20 > len(name) >= 1:
                name_status = namecheck(name)
                if name_status == 'Used':
                    print("Nimi jo käytössä, keksi parempi.")
                    continue
                elif name_status == 'Free':
                    while True:
                        if len(user_information['user_name']) > 0 or user_information['user_password'] == 'reset':
                            break
                        else:
                            print(Style.BRIGHT, Fore.LIGHTRED_EX)
                            userpwd = str(input("Anna käyttäjällesi salasana: "))
                            n = any(char.isdigit() for char in userpwd)
                            b = any(char.isupper() for char in userpwd)

                            if len(userpwd) < 6:
                                print(
                                    "Salasanan täytyy olla vähintään kuusimerkkiä pitkä, sisältää isoja kirjaimia ja numeroita, yritä uutta salasanaa.")
                                continue

                            elif (len(userpwd) >= 6 and n == False):
                                print(
                                    "Salasanan täytyy olla vähintään kuusimerkkiä pitkä, sisältää isoja kirjaimia ja numeroita, yritä uutta salasanaa.")
                                continue

                            elif (len(userpwd) >= 6 and b == False):
                                print(
                                    "Salasanan täytyy olla vähintään kuusimerkkiä pitkä, sisältää isoja kirjaimia ja numeroita, yritä uutta salasanaa.")
                                continue

                            elif len(userpwd) >= 6 and (b == True and n == True):
                                user_information.update({'user_name': name})
                                user_information.update({'user_password': userpwd})
                            print(Style.BRIGHT, Fore.LIGHTRED_EX)
                            print(
                                f"Käyttäjänimesi on: {user_information['user_name']}\nSalasanasi on: {user_information['user_password']}")
                            while True:

                                change_of_mind = input(
                                    "Haluatko jatkaa eteenpäin vai vaihtaa käyttäjätietosi? ['Jatka' tai 'Vaihda']: ").lower()

                                if change_of_mind == 'vaihda':
                                    user_information.update({'user_name': ''})
                                    user_information.update({'user_password': 'reset'})
                                    break

                                elif change_of_mind == 'jatka':
                                    break
                                else:
                                    print("Tarkasta syöte.")
                                    print(Style.BRIGHT, Fore.LIGHTGREEN_EX)
                                    continue
                else:
                    print("Ohjelmisto virhe.")
            else:
                print("Tarkista syöte.")
                continue
        else:
            print("Tarkista syöte.")
            continue
    spawnlocation()


# Testattu - Uuden käyttäjän aloitus lentokentän hakeminen
def starting_airport():
    try:
        with connection.cursor() as cursor:
            sql = f"SELECT airport.name FROM airport WHERE airport.type NOT IN ('heliport', 'closed', 'seaplane_base', 'balloonport') ORDER BY RAND() LIMIT 1;"
            cursor.execute(sql)
            starting_airport = cursor.fetchone()

            sql2 = f"SELECT airport.ident FROM airport WHERE airport.name = '{starting_airport[0]}';"
            cursor.execute(sql2)
            starting_airport_ident = cursor.fetchone()

            sql3 = f"SELECT country.name, country.continent FROM country, airport WHERE airport.name = '{starting_airport[0]}' and airport.iso_country = country.iso_country;"
            cursor.execute(sql3)
            startingcountry_and_continent = cursor.fetchone()

            # Aloitus rahasumman hakeminen:
            starting_money = int(random.randint(5000, 20000))

            # Aloitus Komponenttien tallennus sanakirjaan:
            # Balance
            user_information.update({'balance': starting_money})
            # Aloitus lentokenttä
            user_information.update({'current_airport': starting_airport[0]})
            # Aloitus maa
            user_information.update({'current_country': startingcountry_and_continent[0]})
            # Aloitus maanosa
            user_information.update({'current_continent': startingcountry_and_continent[1]})
            # Aloitus lentokentän ICAO-koodi
            user_information.update({'current_icao_code': starting_airport_ident[0]})

    except pymysql.MySQLError as e:
        print(f"Tietokantavirhe: {e}")

    except Exception as e:
        print(f"Satunnaisvirhe: {e}")


# Testattu - Tallentaa uuden käyttäjän tiedot
def spawnlocation():
    # Pelaajan lentokentän valinta aloittaessa peliä, sekä pelaajan aloitusraha väliltä $5000-$20000:
    if user_information['current_airport'] == '':
        print(f"\nHei {user_information['user_name']}!")
        print("Peli on alkamassa ja haemme vielä aloituslentokentän, sekä aloitusrahan! Saat myös aloitustarinasi: ")
        starting_story = [
            'Krallion sillan vakio asukki. Krallion silta jouduttiin purkamaan, jonka takia hänen lämmin kotinsa tuhoutui, paitsi talvisin. Hän kerrytti rahavarantoaan keräilemällä pulloja, ja alkoi tämän jälkeen matkustella ympäri maailmaa samalla striimaten lentojaan ja antaen näin ilmaisen mainoksen lentoyhtiöille. Hän asetti itselleen tavoitteen saada kasaan $100 000 ja eläköityä tämän saavutettuaan.',

            'Hän oli vuosien 2001-2025 miljoona varallisuudessaan uiskenteleva ökyukko. Kaikki kuitenkin romahti, kun hän oli sijoittanut kaiken varallisuutensaPEPE-coiniin ja se romahti arvossaan eikä enään ikinä noussut. Rahaa hänelle jäi sen verran, että hän päätti matkustaa ympäri maailmaa, samalla tienaten vierailemillaan lentokentillä rahaa, myymällä erittäin kalliita italialaisia pukujen aluspaitoja.',

            'Lyhyt, sluiba joka asusti kauppiksen penkillä. Yksi höröttävä korva. Hänen täytyi myydä velkojen takia PC. Ei menestynyt bisnesmiehenä kauppisopintojensa jälkeen ja alkoi uhkapeliaddiktiksi, joka lopulta oli velkaa jopa Suomen presidentille. Presidentti antoi hänelle tehtävän kerryttää vierailemissaan maissa itselleen varallisuutta keinoilla millä hyvänsä.'
        ]
        print('')
        print('')
        print(Style.BRIGHT, Fore.LIGHTRED_EX)
        tarina = random.choice(starting_story)
        if tarina == starting_story[0]:
            print("Olet köyhä ukko, tarinasi on seuraava: ")
            print(tarina)
            print('')
        elif tarina == starting_story[1]:
            print("Olet menestynyt liikemies, tarinasi on seuraava: ")
            print(tarina)
            print('')
        else:
            print("Olet Ville 'PP' 'Purpola', tarinasi on seuraava: ")
            print(tarina)
            print('')
        while True:
            start = input("Paina [Enter] jatkaaksesi")
            if start == '':
                break
            else:
                print('Tarkista syöte.')

        timer1 = time.time()
        starting_airport()
        timer2 = time.time() - timer1

        print(Style.BRIGHT, Fore.LIGHTRED_EX)
        print(
            f"Aloitus lentokentäksesi on valikoitunut: {user_information['current_airport']}, {user_information['current_country']}, {user_information['current_continent']}\nLentokentän valitsemisessa kesti n. {round(timer2, 2)} sekuntia.\nAloitusrahasi on: [${user_information['balance']}]")
        while True:
            enter = str(input("Palaa aloitusvalikkoon kirjautuneena ja tallenna nykyiset tiedot painamalla [Enter]"))
            if enter == '':
                save_data()
                break
            else:
                print('Tarkista syöte.')
        print(Style.BRIGHT, Fore.LIGHTGREEN_EX)
        gamestart()
    # Peli alkaa heti, jos käyttäjän nykyinen lentokenttä antaa arvon:
    elif user_information['current_airport']:
        game_generator_1()

    else:
        print("Ohjelman käynnistyksessä ilmeni virhe.")


# Game generation - MAIN (PELI ON MAHDOLLISTA LOPETTAA ja TALLENTAA TÄSSÄ)
def game_generator_1():
    1


gamestart()

nimi = {user_information['user_name']}


def casinostart(nick):
    print("\nTervetuloa kasinolle!")
    print("Valitse jokin seuraavista vaihtoehdoista:")
    print("1. Aloita peli")
    print("2. Tarkista saldo")
    print("3. Poistu kasinolta")
    user_data = fetch_user_statistics()
    if not user_data:
        print("Käyttäjätietoja ei löytynyt.")
        return

    # Tarkista, että user_data sisältää "User balance:"-rivin
    if "User balance:" not in user_data:
        print("Virhe: Käyttäjätiedoista puuttuu saldo.")
        return

    try:
        # Etsi 'balance'-rivi ja jäsennä se
        balance_line = [line for line in user_data.split('\n') if line.startswith("User balance:")][0]
        balance_str = balance_line.split(': ')[1]  # Poimi saldon arvo (esim. "[121773]")

        # Poista hakasulkeet ja muunna kokonaisluvuksi
        balance_str = balance_str.replace('[', '').replace(']', '')  # Poista hakasulkeet
        balance = int(balance_str)  # Muunna kokonaisluvuksi

        entire_balance = balance
    except (IndexError, ValueError) as e:
        print(f"Virhe: Saldoa ei voitu jäsentää. Virheen tiedot: {e}")
    while True:
        valinta = input("Syötä valintasi (1-3): ")

        if valinta == '1':
            print("\nValitsit pelin aloittamisen.")
            kasinon_valikko(nick, entire_balance)

        elif valinta == '2':
            print("\nValitsit saldon tarkistamisen.")
            nayta_saldo()

        elif valinta == '3':
            print("\nKiitos käynnistä! Tervetuloa uudelleen.")
            break

        else:
            print("Virheellinen valinta. Valitse 1, 2 tai 3.")


def kasinon_valikko(nick, entire_balance):
    print("\nValitse peli:")
    print("1. Arvaa numero")
    print("2. Nopat")
    print("3. Kolikkopeli (Slots)")
    print("4. Palaa päävalikkoon")

    while True:
        valinta = input("Syötä valintasi (1-4): ")

        if valinta == '1':
            arvaa_numero(nick, entire_balance)

        elif valinta == '2':
            noppapeli(nick, entire_balance)

        elif valinta == '3':
            kolikkopeli(nick, entire_balance)

        elif valinta == '4':
            casinostart(nick)

        else:
            print("Virheellinen valinta. Valitse 1, 2, 3 tai 4.")


def nayta_saldo():
    user_data = fetch_user_statistics()
    if not user_data:
        print("Käyttäjätietoja ei löytynyt.")
        return

    # Tarkista, että user_data sisältää "User balance:"-rivin
    if "User balance:" not in user_data:
        print("Virhe: Käyttäjätiedoista puuttuu saldo.")
        return

    try:
        # Etsi 'balance'-rivi ja jäsennä se
        balance_line = [line for line in user_data.split('\n') if line.startswith("User balance:")][0]
        balance_str = balance_line.split(': ')[1]  # Poimi saldon arvo (esim. "[121773]")

        # Poista hakasulkeet ja muunna kokonaisluvuksi
        balance_str = balance_str.replace('[', '').replace(']', '')  # Poista hakasulkeet
        balance = int(balance_str)  # Muunna kokonaisluvuksi

        entire_balance = balance
        return print(f"Nykyinen saldosi:{entire_balance}")
    except (IndexError, ValueError) as e:
        print(f"Virhe: Saldoa ei voitu jäsentää. Virheen tiedot: {e}")


def arvaa_numero(nick, entire_balance):
    print("\nTervetuloa peliin 'Arvaa numero'!")
    print("Sinulla on 3 yritystä arvata numero väliltä 1-10.")

    panos = int(input("Syötä panoksesi: "))

    if entire_balance < panos:
        print(f"Sinulla ei ole tarpeeksi rahaa. Nykyinen saldosi: ${entire_balance}.")
        return

    entire_balance -= panos  # Vähennetään panos
    numero = random.randint(1, 10)
    yritykset = 3

    while yritykset > 0:
        arvaus = int(input("Syötä arvauksesi: "))
        if arvaus == numero:
            print("Onneksi olkoon! Arvasit oikein!")
            voitto = panos * 2  # Voitto
            cursor = connection.cursor()

            new_balance = entire_balance + voitto
            update_sql = """
                                UPDATE game 
                                SET balance = %s 
                                WHERE nick = %s;
                                """
            cursor.execute(update_sql, (new_balance, nick))
            print(
                f"Pelaaja {nick} pelaaja voitti kasinossa : {voitto}\n\n\n")

            cursor.close()
            nayta_saldo()
            return
        else:
            yritykset -= 1
            print(f"Väärin! Yrityksiä jäljellä: {yritykset}")

    print(f"Valitettavasti hävisit. Oikea numero oli: {numero}.")
    cursor = connection.cursor()

    new_balance = entire_balance - panos
    update_sql = """
                                    UPDATE game 
                                    SET balance = %s 
                                    WHERE nick = %s;
                                    """
    cursor.execute(update_sql, (new_balance, nick))

    cursor.close()
    nayta_saldo()


def noppapeli(nick, entire_balance):
    print("\nTervetuloa peliin 'Nopat'!")
    print("Sinä ja tietokone heitätte noppaa. Suurempi silmäluku voittaa.")

    panos = int(input("Syötä panoksesi: "))

    if entire_balance < panos:
        print(f"Sinulla ei ole tarpeeksi rahaa. Nykyinen saldosi: ${entire_balance}.")
        return

    entire_balance -= panos  # Vähennetään panos
    pelaajan_heitto = random.randint(1, 6)
    tietokoneen_heitto = random.randint(1, 6)

    print(f"Sinä heitit: {pelaajan_heitto}")
    print(f"Tietokone heitti: {tietokoneen_heitto}")

    if pelaajan_heitto > tietokoneen_heitto:
        voitto = panos * 2  # Voitto
        cursor = connection.cursor()

        new_balance = entire_balance + voitto
        update_sql = """
                                        UPDATE game 
                                        SET balance = %s 
                                        WHERE nick = %s;
                                        """
        cursor.execute(update_sql, (new_balance, nick))
        print(
            f"Pelaaja {nick} pelaaja voitti kasinossa : {voitto}\n\n\n")
        cursor.close()
    elif pelaajan_heitto < tietokoneen_heitto:
        print("Sinä hävisit.")
        cursor = connection.cursor()

        havio = entire_balance - panos * 0.5
        update_sql = """
                                            UPDATE game 
                                            SET balance = %s 
                                            WHERE nick = %s;
                                            """
        cursor.execute(update_sql, (havio, nick))

        cursor.close()
    else:
        print("Tasapeli! Panosi palautetaan.")
        # Palautetaan panos

    nayta_saldo()


def kolikkopeli(nick, entire_balance):
    print("\nTervetuloa peliin 'Kolikkopeli (Slots)'!")
    print("Kolikkopelissä pyöräytät kolme rullaa. Saat 3 yritystä.")
    print("Jos 2 symbolia täsmää, voitit panoksesi. Jos 3 symbolia täsmää, voitit panoksesi kaksinkertaisena!")

    panos = int(input("Syötä panoksesi per yritys: "))

    if entire_balance < panos:
        print(f"Sinulla ei ole tarpeeksi rahaa. Nykyinen saldosi: ${entire_balance}.")
        return

    yritykset = 3
    total_winnings = 0

    for yritys in range(1, yritykset + 1):
        print(f"\nYritys {yritys}:")
        print("Haluatko pyöräyttää rullat? (k/e)")
        valinta = input().lower()

        if valinta != 'k':
            print("Lopetit pelin kesken.")
            break

        entire_balance -= panos  # Vähennetään panos
        symbolit = ["🍒", "🍋", "🍊", "⭐", "🔔", "7"]
        rulla1 = random.choice(symbolit)
        rulla2 = random.choice(symbolit)
        rulla3 = random.choice(symbolit)

        print(f"[{rulla1}] [{rulla2}] [{rulla3}]")

        matches = 0
        if rulla1 == rulla2:
            matches += 2
        if rulla2 == rulla3:
            matches += 2
        if rulla1 == rulla3:
            matches += 2

        if matches >= 2:
            if rulla1 == rulla2 == rulla3:

                voitto = panos * 3  # Voitto
                cursor = connection.cursor()

                new_balance = entire_balance + voitto
                update_sql = """
                                                        UPDATE game 
                                                        SET balance = %s 
                                                        WHERE nick = %s;
                                                        """
                cursor.execute(update_sql, (new_balance, nick))
                print(
                    f"Pelaaja {nick} Voitit panoksesi kolmekertaisena : {voitto}\n\n\n")

                cursor.close()

            else:

                voitto = panos * 2  # Voitto
                cursor = connection.cursor()

                new_balance = entire_balance + voitto
                update_sql = """
                                                                        UPDATE game 
                                                                        SET balance = %s 
                                                                        WHERE nick = %s;
                                                                        """
                cursor.execute(update_sql, (new_balance, nick))
                print(
                    f"Pelaaja {nick} Voitit panoksesi kaksinkertaisena : {voitto}\n\n\n")

                cursor.close()

                print("Kaksi oikein! Voitit panoksesi 2 kertaisena!")

        else:
            print("Ei voittoa tällä yrityksellä.")

    nayta_saldo()


def current_icao(nick):
    cursor = connection.cursor()
    try:
        icao_code_query = "SELECT current_icao_code FROM game WHERE nick = %s;"
        cursor.execute(icao_code_query, (nick,))
        result = cursor.fetchone()

        if result:
            return result[0]
        else:
            print(f"Pelaajalle {nick} ei löytynyt ICAO-koodia.")
            return None
    finally:
        cursor.close()


# Ohjelma ottaa icaon koordinaatit ja antaa calculate_distance funktiolle
def get_airport_coordinates(icao_code):
    cursor = connection.cursor()
    try:
        sql = """
            SELECT airport.latitude_deg, airport.longitude_deg
            FROM airport
            WHERE airport.ident = %s;
        """
        cursor.execute(sql, (icao_code,))
        result = cursor.fetchone()

        if result:
            return result[0], result[1]
        else:
            print(f"Ei löytynyt koordinaatteja ICAO-koodille {icao_code}")
            return None
    finally:
        cursor.close()


# laskee uuden ja vanhan lentokentän välissä
def calculate_distance(new_icao, old_icao):
    coords_1 = get_airport_coordinates(new_icao)
    coords_2 = get_airport_coordinates(old_icao)

    if coords_1 and coords_2:
        distance = geodesic(coords_1, coords_2).kilometers

        return distance
    else:
        print("Jokin ICAO-koodin tiedoista puuttuu.")
        return 0


# Function to ask the player for an airport choice
def airport_kysely(old_icao, nick):
    print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nValitse lentokenttä seuraavista vaihtoehdoista:\n\n")
    airports = []  # Store airports to match user input
    used_continents = set()  # Käytettyjen maanosien joukko

    # Hae nykyisen lentokentän koordinaatit
    old_coords = get_airport_coordinates(old_icao)
    if not old_coords:
        print("Nykyisen lentokentän koordinaatteja ei löytynyt.")
        return None

    while len(airports) < 4:  # Valitaan 4 eri lentokenttää
        continent, country, airport_name, valicao_code = get_airport()  # Hae lentokentän tiedot

        # Tarkista, että maanosa ei ole jo käytetty
        if continent and country and airport_name and valicao_code and continent not in used_continents:
            # Hae uuden lentokentän koordinaatit
            new_coords = get_airport_coordinates(valicao_code)
            if new_coords:
                # Laske etäisyys nykyisestä lentokentästä
                distance = geodesic(old_coords, new_coords).kilometers
                # Laske rahamäärä maanosan perusteella
                money = calculate_money_based_on_continent(continent, distance)
                # Lisää lentokenttä listaan
                airports.append((len(airports) + 1, continent, country, airport_name, valicao_code, distance, money))
                used_continents.add(continent)
            else:
                print(f"Ei löytynyt koordinaatteja lentokentälle {valicao_code}.")

    # Näytä lentokentät ja niiden tiedot
    for airport in airports:
        print(
            f"{airport[0]}. {airport[1]} - {airport[2]}: {airport[3]} – Etäisyys: {airport[5]:.2f} km - Saama rahamäärä: {airport[6]:.0f} usd")

    # Kysy pelaajalta valinta

    while True:
        user_choice = int(input("\n\nValitse lentokenttä numeron mukaan: "))
        if user_choice in [1, 2, 3, 4]:
            break
        else:
            print("Tarkista syöte.")
            continue

    # palauta valittu lentokenttä
    if 1 <= user_choice <= 4:
        selected_airport = airports[user_choice - 1]
        print(
            f"\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nValitsit lentokentän:\n{selected_airport[3]} ({selected_airport[1]}, {selected_airport[2]}) ")
        return selected_airport


def calculate_money_based_on_continent(continent, distance):
    # Määritä rahamäärä maanosan perusteella
    if continent == "SA":
        return distance * 2
    elif continent == "AF":
        return distance * 1.5
    elif continent == "AN":
        return distance * 0.8
    else:
        return distance


# laittaa kilometrit tietokantaan
def update_distance(nick, additional_distance):
    cursor = connection.cursor()
    try:

        select_query = "SELECT distance_km FROM game WHERE nick = %s;"
        cursor.execute(select_query, (nick,))
        result = cursor.fetchone()

        if result:
            current_distance = result[0]
            new_distance = current_distance + additional_distance

            #
            update_query = """
            UPDATE game
            SET distance_km = distance_km + %s
            WHERE nick = %s;
            """
            cursor.execute(update_query, (additional_distance, nick))


        else:
            print(f"Pelaajaa {nick} ei löytynyt tietokannasta.")
    except pymysql.MySQLError as e:
        print(f"Error updating player distance: {e}")
    finally:
        cursor.close()


# Random valinta lenttokentistä
def get_airport():
    cursor = connection.cursor()
    try:
        # maanosa
        randcon_query = "SELECT continent FROM country ORDER BY RAND() LIMIT 1;"
        cursor.execute(randcon_query)
        continent = cursor.fetchone()[0]

        # maa
        randmaa_query = """
            SELECT name
            FROM country
            WHERE continent = %s
            ORDER BY RAND()
            LIMIT 1;
        """
        cursor.execute(randmaa_query, (continent,))
        country = cursor.fetchone()[0]

        # lenttokenttä
        airport_type = "large_airport"
        sql = """
            SELECT airport.name, airport.ident
            FROM airport
            JOIN country ON airport.iso_country = country.iso_country
            WHERE country.name = %s AND airport.type = %s
            LIMIT 1;
        """
        cursor.execute(sql, (country, airport_type))

        # ICAO
        result = cursor.fetchone()

        if result is None:
            return None, None, None, None

        airport_name, icao_code = result

        return continent, country, airport_name, icao_code

    finally:
        cursor.close()


# laittaa uusimmat tiedot tietokantaan
def update_user_data(selected_airport):
    cursor = connection.cursor()
    try:
        continent = selected_airport[1]
        country = selected_airport[2]
        airport_name = selected_airport[3]
        icao_code = selected_airport[4]
        x1 = +1

        update_query = """
        UPDATE game 
        SET current_airport = %s, 
            current_country = %s, 
            current_icao_code = %s, 
            current_continent = %s,
            visited_countries = visited_countries + %s
        WHERE nick = %s;
        """
        cursor.execute(update_query, (
            airport_name,
            country,
            icao_code,
            continent,
            x1,
            nimi
        ))



    except pymysql.MySQLError as e:
        print(f"Error updating user data: {e}")
    finally:
        cursor.close()


def check_continent(nick, distance):
    cursor = connection.cursor()
    try:
        # Hae pelaajan nykyinen maanosa ja saldo
        sql = """
        SELECT current_continent, balance 
        FROM game 
        WHERE nick = %s;
        """
        cursor.execute(sql, (nick,))
        result = cursor.fetchone()

        if result:
            current_continent, balance = result

            # (Etelä-Amerikka)
            if current_continent == "SA":

                randbalance = random.randint(1, 5)
                if randbalance == 1:
                    new_balance = balance + distance
                    nolla = new_balance * 0
                    update_sql = """
                                        UPDATE game 
                                        SET balance = %s 
                                        WHERE nick = %s;
                                        """
                    cursor.execute(update_sql, (0, nick))
                    print(
                        f"Pelaaja {nick} lensi Etelä-Amerikkaan, hänet ammuttiin ja varastetiin kaikki rahat. Saldo: {balance} -> {nolla}\n\n\n")


                else:

                    new_balance = balance + distance * 2
                    update_sql = """
                    UPDATE game 
                    SET balance = %s 
                    WHERE nick = %s;
                    """
                    cursor.execute(update_sql, (new_balance, nick))
                    print(
                        f"Pelaaja {nick} lensi Etelä-Amerikkaan ja sai 2x palkan riskisestä työstä. Saldo : {balance} -> {new_balance}\n\n\n")

            if current_continent == "NA":
                new_balance = balance + distance
                update_sql = """
                UPDATE game 
                SET balance = %s 
                WHERE nick = %s;
                """
                cursor.execute(update_sql, (new_balance, nick))
                print(
                    f"Pelaaja {nick} lensi Etelä-Amerikkaan. Saldo: {balance} -> {new_balance} \n\n\n(0)   Pelaa kasinoo            Paina 0")

            # AFRIKKA
            if current_continent == "AF":

                randbalance = random.randint(1, 4)
                if randbalance == 1:
                    new_balance = balance + distance * 1.5
                    puolitettu = new_balance / 2
                    update_sql = """
                                                        UPDATE game 
                                                        SET balance = %s 
                                                        WHERE nick = %s;
                                                        """
                    cursor.execute(update_sql, (puolitettu, nick))
                    print(
                        f"Pelaaja {nick} lensi AFRIKKAAN, hänet ryöstettiin ja varastetiin puolet rahoista. Saldo: {balance} -> {puolitettu}\n\n\n")


                else:

                    new_balance = balance + distance * 1.5
                    update_sql = """
                    UPDATE game 
                    SET balance = %s 
                    WHERE nick = %s;
                    """
                    cursor.execute(update_sql, (new_balance, nick))
                    print(f"Pelaaja {nick} on AFRIKASSA. Saldoo: {balance} -> {new_balance}\n\n\n")
            # OCEANIA
            if current_continent == "OC":
                new_balance = balance + distance
                randbalance = random.randint(1, 3)
                if randbalance == 1:
                    if new_balance > 20000:
                        lääkerahat = new_balance - 20000
                        update_sql = """
                                                                            UPDATE game 
                                                                            SET balance = %s 
                                                                            WHERE nick = %s;
                                                                            """
                        cursor.execute(update_sql, (lääkerahat, nick))
                        print(
                            f"Pelaaja {nick} lensi Oseaniaan. Hänet puri tappava käärme, hän maksoi 20 000 vastamyrkystä. Saldo: {balance} -> {lääkerahat}\n\n\n")
                    else:

                        update_sql = """
                                                                                                    UPDATE game 
                                                                                                    SET balance = %s 
                                                                                                    WHERE nick = %s;
                                                                                                    """
                        cursor.execute(update_sql, (0, nick))
                        print(
                            f"Pelaaja {nick} lensi Oseaniaan. Hänet puri tappava käärme, \n piti maksaa 20 000 vastamyrkystä, mutta saldo ei riittäny, joten pelaaja kuoli.")

                else:
                    new_balance = balance + distance
                    update_sql = """
                    UPDATE game 
                    SET balance = %s 
                    WHERE nick = %s;
                    """
                    cursor.execute(update_sql, (new_balance, nick))
                    print(
                        f"Pelaaja {nick} lensi Oseaniaan. Tuurilla väisti tappavan käärmen Saldo: {balance} -> {new_balance}\n\n\n")
            # Antartica
            if current_continent == "AN":
                # Tuplaa saldo
                new_balance = balance + distance * 0.8
                update_sql = """
                UPDATE game 
                SET balance = %s 
                WHERE nick = %s;
                """
                cursor.execute(update_sql, (new_balance, nick))
                print(f"Pelaaja {nick} lensi Antartikaan. Saldo: {balance} -> {new_balance}\n\n\n")

            if current_continent == "EU":
                # Tuplaa saldo

                new_balance = balance + distance
                update_sql = """
                UPDATE game 
                SET balance = %s 
                WHERE nick = %s;
                """
                cursor.execute(update_sql, (new_balance, nick))
                print(f"Pelaaja {nick} on EUROOPASSA. Saldo: {balance} -> {new_balance}\n\n\n")

            if current_continent == "AS":
                new_balance = balance + distance
                randbalance = random.randint(1, 3)
                if randbalance == 1:
                    if new_balance > 15000:
                        lentokonerahat = new_balance - 15000
                        update_sql = """
                                                                                            UPDATE game 
                                                                                            SET balance = %s 
                                                                                            WHERE nick = %s;
                                                                                            """
                        cursor.execute(update_sql, (lentokonerahat, nick))
                        print(
                            f"Pelaaja {nick} lensi Aasian. Maanjäristys tuhosi lentokoneen. Maksoi 15 000 sen korjaamisesta. Saldo: {balance} -> {lentokonerahat}\n\n\n")
                    else:

                        update_sql = """
                                                                                                                    UPDATE game 
                                                                                                                    SET balance = %s 
                                                                                                                    WHERE nick = %s;
                                                                                                                    """
                        cursor.execute(update_sql, (0, nick))
                        print(
                            f"Pelaaja {nick} lensi Aasian. Maanjäristys tuhosi lentokoneen. Pelaajalla ei ollut riittävästi saldoa n\ pelaaja elää onnellisen elämän siinä maassa vanhuuten ja kuolee \n Loppu")
                else:
                    new_balance = balance + distance
                    update_sql = """
                    UPDATE game 
                    SET balance = %s 
                    WHERE nick = %s;
                    """
                    cursor.execute(update_sql, (new_balance, nick))
                    print(f"Pelaaja {nick} on Aasissa. Saldo: {balance} -> {new_balance}\n\n\n")

        else:
            print(f"Pelaajaa {nick} ei löytynyt tietokannasta.")

    except pymysql.MySQLError as e:
        print(f"Tietokantavirhe: {e}")
    finally:
        cursor.close()


def main(nimi):
    while True:
        # ottaa vanhan icao
        old_icao = current_icao(nimi)
        if not old_icao:
            print("Current ICAO code not found for the player.")
            return

        # ottaa uuden ja vanhan icao arvon
        selected_airport1 = airport_kysely(old_icao, nimi)
        new_icao = selected_airport1[4]

        # laskee kahden lentokentän välinen kilometrit
        distance = calculate_distance(old_icao, new_icao)

        # laittaa kilometrit jos se lentää enenmmän kuin 0
        if distance > 0:
            update_distance(nimi, distance)

        # laittaa tiedot tietokantaan
        update_user_data(selected_airport1)

        # mikä maanosa
        check_continent(nimi, distance)

        check_player_status()
        print(Style.BRIGHT, Fore.LIGHTGREEN_EX)

        def continue12():
            print(
                "(I)      Lennä uuteen lentokenttään     Paina 1 \n"
                "(II)     Lopeta peli                    Paina 2\n"
                "(III)    Katso statistiikka pelistä     Paina 3 \n"
                "(IV)     Mene aloitus-sivulle           Paina 4 \n\n")
            return input("Valitse komento numeron mukaan: ")

        usinp = continue12()  # Käyttäjän syöte tallennetaan muuttujaan `usinp`

        if usinp == "1":  # Vertaile merkkijonolla "1"
            print("Lennetään uuteen lentokenttään...")
            continue


        elif usinp == "2":
            print("Kiitos pelistä! Näkemiin.")
            break  # Lopeta silmukka ja pääohjelma

        elif usinp == "3":
            data = fetch_user_statistics()
            print(f"\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nKäyttäjän [{user_information['user_name']}] Tiedot\n + {data} \n")

            continue12()


        elif usinp == "4":
            gamestart()





        elif usinp == "0":
            print("Kiitos pelistä! Näkemiin.")
            print("WELCOME TO CASINO")
            casinostart(nimi)


        else:
            print("Väärä syöttö, kokeile uudestaan")
            continue12()


main(nimi)

connection.close()

