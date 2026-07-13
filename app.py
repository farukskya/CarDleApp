from flask import Flask, render_template, request, jsonify, session
import random

app = Flask(__name__)
app.secret_key = "cardle_gizli_anahtar_123"

# 200 Araçlık Kallavi Türkiye Veri Tabanı
araclar = [
    # --- İLK 86 ARAÇ (Eskiler Korundu) ---
    {"marka": "Fiat", "model": "Linea", "kasa": "Sedan", "yakit": "Dizel", "motor_tipi": "1.3 MultiJet", "yil": "2007-2017", "ulke": "İtalya"},
    {"marka": "Fiat", "model": "Albea", "kasa": "Sedan", "yakit": "Dizel", "motor_tipi": "1.3 MultiJet", "yil": "2002-2012", "ulke": "İtalya"},
    {"marka": "Fiat", "model": "Punto", "kasa": "Hatchback", "yakit": "Benzin", "motor_tipi": "1.4 Fire", "yil": "2005-2018", "ulke": "İtalya"},
    {"marka": "Renault", "model": "Symbol", "kasa": "Sedan", "yakit": "Dizel", "motor_tipi": "1.5 dCi", "yil": "2008-2021", "ulke": "Fransa"},
    {"marka": "Renault", "model": "Fluence", "kasa": "Sedan", "yakit": "Dizel", "motor_tipi": "1.5 dCi", "yil": "2009-2016", "ulke": "Fransa"},
    {"marka": "Renault", "model": "Kadjar", "kasa": "SUV", "yakit": "Dizel", "motor_tipi": "1.5 dCi", "yil": "2015-2022", "ulke": "Fransa"},
    {"marka": "Hyundai", "model": "Accent Era", "kasa": "Sedan", "yakit": "Dizel", "motor_tipi": "1.5 CRDi", "yil": "2006-2012", "ulke": "Güney Kore"},
    {"marka": "Hyundai", "model": "Accent Blue", "kasa": "Sedan", "yakit": "Dizel", "motor_tipi": "1.6 CRDi", "yil": "2011-2019", "ulke": "Güney Kore"},
    {"marka": "Hyundai", "model": "Getz", "kasa": "Hatchback", "yakit": "Dizel", "motor_tipi": "1.5 CRDi", "yil": "2002-2011", "ulke": "Güney Kore"},
    {"marka": "Toyota", "model": "Auris", "kasa": "Hatchback", "yakit": "Dizel", "motor_tipi": "1.4 D-4D", "yil": "2007-2018", "ulke": "Japonya"},
    {"marka": "Toyota", "model": "C-HR", "kasa": "SUV", "yakit": "Hibrit", "motor_tipi": "1.8", "yil": "2016-2026", "ulke": "Japonya"},
    {"marka": "Honda", "model": "Jazz", "kasa": "Hatchback", "yakit": "Benzin", "motor_tipi": "1.4 i-VTEC", "yil": "2002-2026", "ulke": "Japonya"},
    {"marka": "Volkswagen", "model": "Jetta", "kasa": "Sedan", "yakit": "Dizel", "motor_tipi": "1.6 TDI", "yil": "2005-2018", "ulke": "Almanya"},
    {"marka": "Volkswagen", "model": "Caddy", "kasa": "Ticari", "yakit": "Dizel", "motor_tipi": "2.0 TDI", "yil": "2004-2026", "ulke": "Almanya"},
    {"marka": "Ford", "model": "Fiesta (Eski)", "kasa": "Hatchback", "yakit": "Dizel", "motor_tipi": "1.4 TDCi", "yil": "2008-2017", "ulke": "Amerika"},
    {"marka": "Ford", "model": "Focus (Eski)", "kasa": "Sedan", "yakit": "Dizel", "motor_tipi": "1.6 TDCi", "yil": "2011-2018", "ulke": "Amerika"},
    {"marka": "Ford", "model": "Mondeo", "kasa": "Sedan", "yakit": "Dizel", "motor_tipi": "2.0 TDCi", "yil": "2014-2022", "ulke": "Amerika"},
    {"marka": "Opel", "model": "Astra J", "kasa": "Sedan", "yakit": "Dizel", "motor_tipi": "1.3 CDTI", "yil": "2012-2020", "ulke": "Almanya"},
    {"marka": "Opel", "model": "Insignia", "kasa": "Sedan", "yakit": "Dizel", "motor_tipi": "1.6 CDTI", "yil": "2008-2022", "ulke": "Almanya"},
    {"marka": "Peugeot", "model": "301", "kasa": "Sedan", "yakit": "Dizel", "motor_tipi": "1.6 HDi", "yil": "2012-2021", "ulke": "Fransa"},
    {"marka": "Peugeot", "model": "508", "kasa": "Sedan", "yakit": "Dizel", "motor_tipi": "1.5 BlueHDi", "yil": "2011-2026", "ulke": "Fransa"},
    {"marka": "Citroen", "model": "C3 Aircross", "kasa": "SUV", "yakit": "Benzin", "motor_tipi": "1.2 PureTech", "yil": "2017-2026", "ulke": "Fransa"},
    {"marka": "Skoda", "model": "Scala", "kasa": "Hatchback", "yakit": "Benzin", "motor_tipi": "1.0 TSI", "yil": "2019-2026", "ulke": "Çek Cumhuriyeti"},
    {"marka": "Seat", "model": "Toledo", "kasa": "Sedan", "yakit": "Dizel", "motor_tipi": "1.6 TDI", "yil": "2012-2019", "ulke": "İspanya"},
    {"marka": "Kia", "model": "Ceed", "kasa": "Hatchback", "yakit": "Dizel", "motor_tipi": "1.6 CRDi", "yil": "2012-2026", "ulke": "Güney Kore"},
    {"marka": "Kia", "model": "Cerato", "kasa": "Sedan", "yakit": "Benzin", "motor_tipi": "1.6 MPI", "yil": "2016-2021", "ulke": "Güney Kore"},
    {"marka": "Nissan", "model": "X-Trail", "kasa": "SUV", "yakit": "Dizel", "motor_tipi": "1.6 dCi", "yil": "2014-2026", "ulke": "Japonya"},
    {"marka": "Chevrolet", "model": "Cruze", "kasa": "Sedan", "yakit": "Benzin", "motor_tipi": "1.6", "yil": "2009-2014", "ulke": "Amerika"},
    {"marka": "Chevrolet", "model": "Aveo", "kasa": "Sedan", "yakit": "Dizel", "motor_tipi": "1.3 D", "yil": "2011-2014", "ulke": "Amerika"},
    {"marka": "Dacia", "model": "Logan MCV", "kasa": "Station Wagon", "yakit": "Dizel", "motor_tipi": "1.5 dCi", "yil": "2013-2020", "ulke": "Romanya"},
    {"marka": "Dacia", "model": "Lodgy", "kasa": "MPV", "yakit": "Dizel", "motor_tipi": "1.5 dCi", "yil": "2012-2022", "ulke": "Romanya"},
    {"marka": "Toyota", "model": "Corolla", "kasa": "Sedan", "yakit": "Hibrit", "motor_tipi": "1.8", "yil": "2019-2026", "ulke": "Japonya"},
    {"marka": "Toyota", "model": "Yaris", "kasa": "Hatchback", "yakit": "Benzin", "motor_tipi": "1.5", "yil": "2020-2026", "ulke": "Japonya"},
    {"marka": "Honda", "model": "Civic", "kasa": "Sedan", "yakit": "Benzin", "motor_tipi": "1.5 VTEC", "yil": "2016-2026", "ulke": "Japonya"},
    {"marka": "Honda", "model": "City", "kasa": "Sedan", "yakit": "Benzin", "motor_tipi": "1.5 i-VTEC", "yil": "2021-2026", "ulke": "Japonya"},
    {"marka": "Honda", "model": "HR-V", "kasa": "SUV", "yakit": "Hibrit", "motor_tipi": "1.5 e:HEV", "yil": "2021-2026", "ulke": "Japonya"},
    {"marka": "Volkswagen", "model": "Golf", "kasa": "Hatchback", "yakit": "Benzin", "motor_tipi": "1.5 TSI", "yil": "2012-2026", "ulke": "Almanya"},
    {"marka": "Volkswagen", "model": "Passat", "kasa": "Sedan", "yakit": "Dizel", "motor_tipi": "2.0 TDI", "yil": "2015-2023", "ulke": "Almanya"},
    {"marka": "Volkswagen", "model": "Polo", "kasa": "Hatchback", "yakit": "Benzin", "motor_tipi": "1.0 TSI", "yil": "2017-2026", "ulke": "Almanya"},
    {"marka": "Volkswagen", "model": "Tiguan", "kasa": "SUV", "yakit": "Benzin", "motor_tipi": "1.5 TSI", "yil": "2016-2026", "ulke": "Almanya"},
    {"marka": "Fiat", "model": "Egea", "kasa": "Sedan", "yakit": "Dizel", "motor_tipi": "1.3 MultiJet", "yil": "2015-2026", "ulke": "İtalya"},
    {"marka": "Fiat", "model": "Egea Cross", "kasa": "SUV", "yakit": "Benzin", "motor_tipi": "1.4 Fire", "yil": "2021-2026", "ulke": "İtalya"},
    {"marka": "Fiat", "model": "Fiorino", "kasa": "Ticari", "yakit": "Dizel", "motor_tipi": "1.3 MultiJet", "yil": "2007-2026", "ulke": "İtalya"},
    {"marka": "Fiat", "model": "Panda", "kasa": "Hatchback", "yakit": "Benzin", "motor_tipi": "1.0 Mild Hybrid", "yil": "2012-2026", "ulke": "İtalya"},
    {"marka": "Renault", "model": "Clio", "kasa": "Hatchback", "yakit": "Benzin", "motor_tipi": "1.0 TCe", "yil": "2019-2026", "ulke": "Fransa"},
    {"marka": "Renault", "model": "Megane", "kasa": "Sedan", "yakit": "Benzin", "motor_tipi": "1.3 TCe", "yil": "2016-2026", "ulke": "Fransa"},
    {"marka": "Renault", "model": "Captur", "kasa": "SUV", "yakit": "Benzin", "motor_tipi": "1.3 TCe", "yil": "2020-2026", "ulke": "Fransa"},
    {"marka": "Renault", "model": "Austral", "kasa": "SUV", "yakit": "Mild Hybrid", "motor_tipi": "1.3 Mild Hybrid", "yil": "2023-2026", "ulke": "Fransa"},
    {"marka": "Renault", "model": "Taliant", "kasa": "Sedan", "yakit": "Benzin", "motor_tipi": "1.0 TCe", "yil": "2021-2026", "ulke": "Fransa"},
    {"marka": "Hyundai", "model": "i20", "kasa": "Hatchback", "yakit": "Benzin", "motor_tipi": "1.4 MPI", "yil": "2014-2026", "ulke": "Güney Kore"},
    {"marka": "Hyundai", "model": "i10", "kasa": "Hatchback", "yakit": "Benzin", "motor_tipi": "1.2 MPI", "yil": "2020-2026", "ulke": "Güney Kore"},
    {"marka": "Hyundai", "model": "Elantra", "kasa": "Sedan", "yakit": "Benzin", "motor_tipi": "1.6 MPI", "yil": "2021-2026", "ulke": "Güney Kore"},
    {"marka": "Hyundai", "model": "Tucson", "kasa": "SUV", "yakit": "Dizel", "motor_tipi": "1.6 CRDi", "yil": "2021-2026", "ulke": "Güney Kore"},
    {"marka": "Hyundai", "model": "Bayon", "kasa": "SUV", "yakit": "Benzin", "motor_tipi": "1.4 MPI", "yil": "2021-2026", "ulke": "Güney Kore"},
    {"marka": "Dacia", "model": "Duster", "kasa": "SUV", "yakit": "Dizel", "motor_tipi": "1.5 dCi", "yil": "2010-2026", "ulke": "Romanya"},
    {"marka": "Dacia", "model": "Sandero Stepway", "kasa": "Hatchback", "yakit": "Benzin", "motor_tipi": "1.0 TCe", "yil": "2021-2026", "ulke": "Romanya"},
    {"marka": "Dacia", "model": "Jogger", "kasa": "SUV", "yakit": "LPG", "motor_tipi": "1.0 ECO-G", "yil": "2022-2026", "ulke": "Romanya"},
    {"marka": "Peugeot", "model": "208", "kasa": "Hatchback", "yakit": "Benzin", "motor_tipi": "1.2 PureTech", "yil": "2020-2026", "ulke": "Fransa"},
    {"marka": "Peugeot", "model": "308", "kasa": "Hatchback", "yakit": "Benzin", "motor_tipi": "1.2 PureTech", "yil": "2021-2026", "ulke": "Fransa"},
    {"marka": "Peugeot", "model": "2008", "kasa": "SUV", "yakit": "Dizel", "motor_tipi": "1.5 BlueHDi", "yil": "2019-2026", "ulke": "Fransa"},
    {"marka": "Peugeot", "model": "3008", "kasa": "SUV", "yakit": "Dizel", "motor_tipi": "1.5 BlueHDi", "yil": "2016-2026", "ulke": "Fransa"},
    {"marka": "Opel", "model": "Corsa", "kasa": "Hatchback", "yakit": "Benzin", "motor_tipi": "1.2 PureTech", "yil": "2019-2026", "ulke": "Almanya"},
    {"marka": "Opel", "model": "Astra", "kasa": "Hatchback", "yakit": "Benzin", "motor_tipi": "1.2 Turbo", "yil": "2022-2026", "ulke": "Almanya"},
    {"marka": "Opel", "model": "Mokka", "kasa": "SUV", "yakit": "Benzin", "motor_tipi": "1.2 Turbo", "yil": "2021-2026", "ulke": "Almanya"},
    {"marka": "Opel", "model": "Crossland", "kasa": "SUV", "yakit": "Benzin", "motor_tipi": "1.2 PureTech", "yil": "2017-2024", "ulke": "Almanya"},
    {"marka": "Citroen", "model": "C3", "kasa": "Hatchback", "yakit": "Benzin", "motor_tipi": "1.2 PureTech", "yil": "2016-2026", "ulke": "Fransa"},
    {"marka": "Citroen", "model": "C4", "kasa": "Hatchback", "yakit": "Benzin", "motor_tipi": "1.2 PureTech", "yil": "2020-2026", "ulke": "Fransa"},
    {"marka": "Citroen", "model": "C5 Aircross", "kasa": "SUV", "yakit": "Dizel", "motor_tipi": "1.5 BlueHDi", "yil": "2018-2026", "ulke": "Fransa"},
    {"marka": "Citroen", "model": "C-Elysee", "kasa": "Sedan", "yakit": "Dizel", "motor_tipi": "1.6 BlueHDi", "yil": "2012-2022", "ulke": "Fransa"},
    {"marka": "Skoda", "model": "Fabia", "kasa": "Hatchback", "yakit": "Benzin", "motor_tipi": "1.0 TSI", "yil": "2021-2026", "ulke": "Çek Cumhuriyeti"},
    {"marka": "Skoda", "model": "Octavia", "kasa": "Sedan", "yakit": "Mild Hybrid", "motor_tipi": "1.5 eTSI", "yil": "2020-2026", "ulke": "Çek Cumhuriyeti"},
    {"marka": "Skoda", "model": "Superb", "kasa": "Sedan", "yakit": "Dizel", "motor_tipi": "2.0 TDI", "yil": "2015-2026", "ulke": "Çek Cumhuriyeti"},
    {"marka": "Skoda", "model": "Kamiq", "kasa": "SUV", "yakit": "Benzin", "motor_tipi": "1.0 TSI", "yil": "2019-2026", "ulke": "Çek Cumhuriyeti"},
    {"marka": "Seat", "model": "Ibiza", "kasa": "Hatchback", "yakit": "Benzin", "motor_tipi": "1.0 EcoTSI", "yil": "2017-2026", "ulke": "İspanya"},
    {"marka": "Seat", "model": "Leon", "kasa": "Hatchback", "yakit": "Benzin", "motor_tipi": "1.5 TSI", "yil": "2020-2026", "ulke": "İspanya"},
    {"marka": "Seat", "model": "Arona", "kasa": "SUV", "yakit": "Benzin", "motor_tipi": "1.0 EcoTSI", "yil": "2017-2026", "ulke": "İspanya"},
    {"marka": "Kia", "model": "Picanto", "kasa": "Hatchback", "yakit": "Benzin", "motor_tipi": "1.0 DPI", "yil": "2017-2026", "ulke": "Güney Kore"},
    {"marka": "Kia", "model": "Rio", "kasa": "Hatchback", "yakit": "Benzin", "motor_tipi": "1.4 MPI", "yil": "2017-2023", "ulke": "Güney Kore"},
    {"marka": "Kia", "model": "Stonic", "kasa": "SUV", "yakit": "Benzin", "motor_tipi": "1.4 MPI", "yil": "2017-2026", "ulke": "Güney Kore"},
    {"marka": "Kia", "model": "Sportage", "kasa": "SUV", "yakit": "Mild Hybrid", "motor_tipi": "1.6 CRDi", "yil": "2021-2026", "ulke": "Güney Kore"},
    {"marka": "Ford", "model": "Fiesta", "kasa": "Hatchback", "yakit": "Benzin", "motor_tipi": "1.0 EcoBoost", "yil": "2017-2023", "ulke": "Amerika"},
    {"marka": "Ford", "model": "Focus", "kasa": "Sedan", "yakit": "Dizel", "motor_tipi": "1.5 EcoBlue", "yil": "2018-2026", "ulke": "Amerika"},
    {"marka": "Ford", "model": "Puma", "kasa": "SUV", "yakit": "Mild Hybrid", "motor_tipi": "1.0 EcoBoost", "yil": "2019-2026", "ulke": "Amerika"},
    {"marka": "Nissan", "model": "Micra", "kasa": "Hatchback", "yakit": "Benzin", "motor_tipi": "1.0 IG-T", "yil": "2017-2023", "ulke": "Japonya"},
    {"marka": "Nissan", "model": "Qashqai", "kasa": "SUV", "yakit": "Mild Hybrid", "motor_tipi": "1.3 DIG-T", "yil": "2021-2026", "ulke": "Japonya"},
    {"marka": "Nissan", "model": "Juke", "kasa": "SUV", "yakit": "Benzin", "motor_tipi": "1.0 DIG-T", "yil": "2019-2026", "ulke": "Japonya"},
    
    # --- YENİ EKLENEN 114 ARAÇ (Tofaşlar, Lüksler, Ticari Enişteler vb.) ---
    {"marka": "Tofaş", "model": "Şahin", "kasa": "Sedan", "yakit": "LPG", "motor_tipi": "1.6", "yil": "1988-2002", "ulke": "Türkiye"},
    {"marka": "Tofaş", "model": "Doğan", "kasa": "Sedan", "yakit": "LPG", "motor_tipi": "1.6 SLX", "yil": "1988-2002", "ulke": "Türkiye"},
    {"marka": "Tofaş", "model": "Kartal", "kasa": "Station Wagon", "yakit": "LPG", "motor_tipi": "1.6 SLX", "yil": "1988-2002", "ulke": "Türkiye"},
    {"marka": "Renault", "model": "Toros", "kasa": "Station Wagon", "yakit": "LPG", "motor_tipi": "1.4", "yil": "1989-2000", "ulke": "Türkiye"},
    {"marka": "Renault", "model": "Broadway", "kasa": "Sedan", "yakit": "LPG", "motor_tipi": "1.4", "yil": "1997-2000", "ulke": "Türkiye"},
    {"marka": "Fiat", "model": "Tipo", "kasa": "Hatchback", "yakit": "Benzin", "motor_tipi": "1.6", "yil": "1990-2000", "ulke": "İtalya"},
    {"marka": "Fiat", "model": "Tempra", "kasa": "Sedan", "yakit": "Benzin", "motor_tipi": "2.0 i.e", "yil": "1990-1999", "ulke": "İtalya"},
    {"marka": "Fiat", "model": "Marea", "kasa": "Sedan", "yakit": "Benzin", "motor_tipi": "1.6", "yil": "1996-2007", "ulke": "İtalya"},
    {"marka": "Fiat", "model": "Bravo", "kasa": "Hatchback", "yakit": "Dizel", "motor_tipi": "1.6 MultiJet", "yil": "2007-2014", "ulke": "İtalya"},
    {"marka": "Fiat", "model": "Doblo", "kasa": "Ticari", "yakit": "Dizel", "motor_tipi": "1.3 MultiJet", "yil": "2000-2026", "ulke": "İtalya"},
    {"marka": "Renault", "model": "Kangoo", "kasa": "Ticari", "yakit": "Dizel", "motor_tipi": "1.5 dCi", "yil": "1997-2026", "ulke": "Fransa"},
    {"marka": "Ford", "model": "Tourneo Courier", "kasa": "Ticari", "yakit": "Dizel", "motor_tipi": "1.5 TDCi", "yil": "2014-2026", "ulke": "Amerika"},
    {"marka": "Peugeot", "model": "Rifter", "kasa": "Ticari", "yakit": "Dizel", "motor_tipi": "1.5 BlueHDi", "yil": "2018-2026", "ulke": "Fransa"},
    {"marka": "Citroen", "model": "Berlingo", "kasa": "Ticari", "yakit": "Dizel", "motor_tipi": "1.5 BlueHDi", "yil": "1996-2026", "ulke": "Fransa"},
    {"marka": "Volkswagen", "model": "Transporter", "kasa": "Ticari", "yakit": "Dizel", "motor_tipi": "2.0 TDI", "yil": "1990-2026", "ulke": "Almanya"},
    {"marka": "Ford", "model": "Transit", "kasa": "Ticari", "yakit": "Dizel", "motor_tipi": "2.0 EcoBlue", "yil": "1965-2026", "ulke": "Amerika"},
    {"marka": "Toyota", "model": "Hilux", "kasa": "Pick-up", "yakit": "Dizel", "motor_tipi": "2.4 D-4D", "yil": "2015-2026", "ulke": "Japonya"},
    {"marka": "Mitsubishi", "model": "L200", "kasa": "Pick-up", "yakit": "Dizel", "motor_tipi": "2.2 DI-D", "yil": "2015-2026", "ulke": "Japonya"},
    {"marka": "Volkswagen", "model": "Amarok", "kasa": "Pick-up", "yakit": "Dizel", "motor_tipi": "2.0 TDI", "yil": "2010-2026", "ulke": "Almanya"},
    {"marka": "Ford", "model": "Ranger", "kasa": "Pick-up", "yakit": "Dizel", "motor_tipi": "2.0 EcoBlue", "yil": "2011-2026", "ulke": "Amerika"},
    {"marka": "Isuzu", "model": "D-Max", "kasa": "Pick-up", "yakit": "Dizel", "motor_tipi": "1.9", "yil": "2012-2026", "ulke": "Japonya"},
    {"marka": "Nissan", "model": "Navara", "kasa": "Pick-up", "yakit": "Dizel", "motor_tipi": "2.3 dCi", "yil": "2015-2022", "ulke": "Japonya"},
    {"marka": "Togg", "model": "T10X", "kasa": "SUV", "yakit": "Elektrik", "motor_tipi": "e-Motor", "yil": "2023-2026", "ulke": "Türkiye"},
    {"marka": "Tesla", "model": "Model Y", "kasa": "SUV", "yakit": "Elektrik", "motor_tipi": "Dual Motor", "yil": "2020-2026", "ulke": "Amerika"},
    {"marka": "Tesla", "model": "Model 3", "kasa": "Sedan", "yakit": "Elektrik", "motor_tipi": "Dual Motor", "yil": "2017-2026", "ulke": "Amerika"},
    {"marka": "Porsche", "model": "Taycan", "kasa": "Sedan", "yakit": "Elektrik", "motor_tipi": "e-Motor", "yil": "2019-2026", "ulke": "Almanya"},
    {"marka": "Porsche", "model": "Macan", "kasa": "SUV", "yakit": "Benzin", "motor_tipi": "2.0", "yil": "2014-2026", "ulke": "Almanya"},
    {"marka": "Porsche", "model": "Cayenne", "kasa": "SUV", "yakit": "Benzin", "motor_tipi": "3.0 V6", "yil": "2002-2026", "ulke": "Almanya"},
    {"marka": "Mercedes-Benz", "model": "C-Serisi", "kasa": "Sedan", "yakit": "Benzin", "motor_tipi": "1.5", "yil": "2014-2026", "ulke": "Almanya"},
    {"marka": "Mercedes-Benz", "model": "E-Serisi", "kasa": "Sedan", "yakit": "Dizel", "motor_tipi": "2.0", "yil": "2016-2026", "ulke": "Almanya"},
    {"marka": "Mercedes-Benz", "model": "A-Serisi", "kasa": "Hatchback", "yakit": "Benzin", "motor_tipi": "1.3", "yil": "2018-2026", "ulke": "Almanya"},
    {"marka": "Mercedes-Benz", "model": "CLA", "kasa": "Sedan", "yakit": "Benzin", "motor_tipi": "1.3", "yil": "2013-2026", "ulke": "Almanya"},
    {"marka": "Mercedes-Benz", "model": "GLA", "kasa": "SUV", "yakit": "Benzin", "motor_tipi": "1.3", "yil": "2014-2026", "ulke": "Almanya"},
    {"marka": "Mercedes-Benz", "model": "GLC", "kasa": "SUV", "yakit": "Dizel", "motor_tipi": "2.0", "yil": "2015-2026", "ulke": "Almanya"},
    {"marka": "Mercedes-Benz", "model": "G-Serisi", "kasa": "SUV", "yakit": "Benzin", "motor_tipi": "4.0 V8", "yil": "1979-2026", "ulke": "Almanya"},
    {"marka": "BMW", "model": "1 Serisi", "kasa": "Hatchback", "yakit": "Benzin", "motor_tipi": "1.5", "yil": "2011-2026", "ulke": "Almanya"},
    {"marka": "BMW", "model": "3 Serisi", "kasa": "Sedan", "yakit": "Benzin", "motor_tipi": "1.6", "yil": "2012-2026", "ulke": "Almanya"},
    {"marka": "BMW", "model": "5 Serisi", "kasa": "Sedan", "yakit": "Dizel", "motor_tipi": "2.0", "yil": "2010-2026", "ulke": "Almanya"},
    {"marka": "BMW", "model": "X1", "kasa": "SUV", "yakit": "Benzin", "motor_tipi": "1.5", "yil": "2015-2026", "ulke": "Almanya"},
    {"marka": "BMW", "model": "X3", "kasa": "SUV", "yakit": "Dizel", "motor_tipi": "2.0", "yil": "2017-2026", "ulke": "Almanya"},
    {"marka": "BMW", "model": "X5", "kasa": "SUV", "yakit": "Dizel", "motor_tipi": "3.0", "yil": "2013-2026", "ulke": "Almanya"},
    {"marka": "BMW", "model": "4 Serisi", "kasa": "Coupe", "yakit": "Benzin", "motor_tipi": "2.0", "yil": "2013-2026", "ulke": "Almanya"},
    {"marka": "Audi", "model": "A3", "kasa": "Hatchback", "yakit": "Benzin", "motor_tipi": "1.5 TFSI", "yil": "2012-2026", "ulke": "Almanya"},
    {"marka": "Audi", "model": "A4", "kasa": "Sedan", "yakit": "Dizel", "motor_tipi": "2.0 TDI", "yil": "2015-2026", "ulke": "Almanya"},
    {"marka": "Audi", "model": "A5", "kasa": "Coupe", "yakit": "Benzin", "motor_tipi": "2.0 TFSI", "yil": "2016-2026", "ulke": "Almanya"},
    {"marka": "Audi", "model": "A6", "kasa": "Sedan", "yakit": "Dizel", "motor_tipi": "2.0 TDI", "yil": "2011-2026", "ulke": "Almanya"},
    {"marka": "Audi", "model": "Q3", "kasa": "SUV", "yakit": "Benzin", "motor_tipi": "1.5 TFSI", "yil": "2018-2026", "ulke": "Almanya"},
    {"marka": "Audi", "model": "Q5", "kasa": "SUV", "yakit": "Dizel", "motor_tipi": "2.0 TDI", "yil": "2017-2026", "ulke": "Almanya"},
    {"marka": "Audi", "model": "Q7", "kasa": "SUV", "yakit": "Dizel", "motor_tipi": "3.0 TDI", "yil": "2015-2026", "ulke": "Almanya"},
    {"marka": "Volvo", "model": "XC40", "kasa": "SUV", "yakit": "Benzin", "motor_tipi": "1.5 T3", "yil": "2017-2026", "ulke": "İsveç"},
    {"marka": "Volvo", "model": "XC60", "kasa": "SUV", "yakit": "Mild Hybrid", "motor_tipi": "2.0 B4", "yil": "2017-2026", "ulke": "İsveç"},
    {"marka": "Volvo", "model": "XC90", "kasa": "SUV", "yakit": "Mild Hybrid", "motor_tipi": "2.0 B5", "yil": "2015-2026", "ulke": "İsveç"},
    {"marka": "Volvo", "model": "S60", "kasa": "Sedan", "yakit": "Mild Hybrid", "motor_tipi": "2.0 B4", "yil": "2019-2026", "ulke": "İsveç"},
    {"marka": "Volvo", "model": "S90", "kasa": "Sedan", "yakit": "Mild Hybrid", "motor_tipi": "2.0 B5", "yil": "2016-2026", "ulke": "İsveç"},
    {"marka": "Volvo", "model": "V40", "kasa": "Hatchback", "yakit": "Dizel", "motor_tipi": "1.6 D2", "yil": "2012-2019", "ulke": "İsveç"},
    {"marka": "Honda", "model": "Accord", "kasa": "Sedan", "yakit": "Benzin", "motor_tipi": "1.5 VTEC", "yil": "2018-2026", "ulke": "Japonya"},
    {"marka": "Honda", "model": "CR-V", "kasa": "SUV", "yakit": "Hibrit", "motor_tipi": "2.0 e:HEV", "yil": "2017-2026", "ulke": "Japonya"},
    {"marka": "Mazda", "model": "3", "kasa": "Hatchback", "yakit": "Benzin", "motor_tipi": "1.5 Skyactiv-G", "yil": "2014-2026", "ulke": "Japonya"},
    {"marka": "Mazda", "model": "6", "kasa": "Sedan", "yakit": "Benzin", "motor_tipi": "2.0 Skyactiv-G", "yil": "2012-2026", "ulke": "Japonya"},
    {"marka": "Mazda", "model": "CX-5", "kasa": "SUV", "yakit": "Benzin", "motor_tipi": "2.0 Skyactiv-G", "yil": "2017-2026", "ulke": "Japonya"},
    {"marka": "Subaru", "model": "Impreza", "kasa": "Hatchback", "yakit": "Benzin", "motor_tipi": "1.6", "yil": "2016-2026", "ulke": "Japonya"},
    {"marka": "Subaru", "model": "Forester", "kasa": "SUV", "yakit": "Hibrit", "motor_tipi": "2.0 e-Boxer", "yil": "2018-2026", "ulke": "Japonya"},
    {"marka": "Subaru", "model": "XV", "kasa": "SUV", "yakit": "Benzin", "motor_tipi": "1.6", "yil": "2017-2026", "ulke": "Japonya"},
    {"marka": "Suzuki", "model": "Swift", "kasa": "Hatchback", "yakit": "Mild Hybrid", "motor_tipi": "1.2", "yil": "2017-2026", "ulke": "Japonya"},
    {"marka": "Suzuki", "model": "Vitara", "kasa": "SUV", "yakit": "Mild Hybrid", "motor_tipi": "1.4 Boosterjet", "yil": "2015-2026", "ulke": "Japonya"},
    {"marka": "Suzuki", "model": "Jimny", "kasa": "SUV", "yakit": "Benzin", "motor_tipi": "1.5", "yil": "2018-2026", "ulke": "Japonya"},
    {"marka": "Alfa Romeo", "model": "Giulietta", "kasa": "Hatchback", "yakit": "Dizel", "motor_tipi": "1.6 JTDm", "yil": "2010-2020", "ulke": "İtalya"},
    {"marka": "Alfa Romeo", "model": "159", "kasa": "Sedan", "yakit": "Dizel", "motor_tipi": "1.9 JTDm", "yil": "2005-2011", "ulke": "İtalya"},
    {"marka": "Alfa Romeo", "model": "Tonale", "kasa": "SUV", "yakit": "Hibrit", "motor_tipi": "1.5 MHEV", "yil": "2022-2026", "ulke": "İtalya"},
    {"marka": "Jeep", "model": "Renegade", "kasa": "SUV", "yakit": "Benzin", "motor_tipi": "1.3 T4", "yil": "2014-2026", "ulke": "Amerika"},
    {"marka": "Jeep", "model": "Compass", "kasa": "SUV", "yakit": "Hibrit", "motor_tipi": "1.3 e-Hybrid", "yil": "2017-2026", "ulke": "Amerika"},
    {"marka": "Jeep", "model": "Grand Cherokee", "kasa": "SUV", "yakit": "Dizel", "motor_tipi": "3.0 V6", "yil": "2011-2026", "ulke": "Amerika"},
    {"marka": "Mini", "model": "Cooper", "kasa": "Hatchback", "yakit": "Benzin", "motor_tipi": "1.5", "yil": "2014-2026", "ulke": "İngiltere"},
    {"marka": "Mini", "model": "Countryman", "kasa": "SUV", "yakit": "Benzin", "motor_tipi": "1.5", "yil": "2017-2026", "ulke": "İngiltere"},
    {"marka": "Land Rover", "model": "Range Rover", "kasa": "SUV", "yakit": "Dizel", "motor_tipi": "3.0 V6", "yil": "2012-2026", "ulke": "İngiltere"},
    {"marka": "Land Rover", "model": "Evoque", "kasa": "SUV", "yakit": "Dizel", "motor_tipi": "2.0 TD4", "yil": "2011-2026", "ulke": "İngiltere"},
    {"marka": "Dacia", "model": "Spring", "kasa": "SUV", "yakit": "Elektrik", "motor_tipi": "e-Motor", "yil": "2021-2026", "ulke": "Romanya"},
    {"marka": "Skoda", "model": "Kodiaq", "kasa": "SUV", "yakit": "Benzin", "motor_tipi": "1.5 TSI", "yil": "2016-2026", "ulke": "Çek Cumhuriyeti"},
    {"marka": "Skoda", "model": "Karoq", "kasa": "SUV", "yakit": "Benzin", "motor_tipi": "1.5 TSI", "yil": "2017-2026", "ulke": "Çek Cumhuriyeti"},
    {"marka": "Skoda", "model": "Favorit", "kasa": "Hatchback", "yakit": "LPG", "motor_tipi": "1.3", "yil": "1987-1995", "ulke": "Çek Cumhuriyeti"},
    {"marka": "Skoda", "model": "Felicia", "kasa": "Hatchback", "yakit": "LPG", "motor_tipi": "1.3", "yil": "1994-2001", "ulke": "Çek Cumhuriyeti"},
    {"marka": "Skoda", "model": "Roomster", "kasa": "MPV", "yakit": "Dizel", "motor_tipi": "1.2 TDI", "yil": "2006-2015", "ulke": "Çek Cumhuriyeti"},
    {"marka": "Seat", "model": "Ateca", "kasa": "SUV", "yakit": "Benzin", "motor_tipi": "1.5 TSI", "yil": "2016-2026", "ulke": "İspanya"},
    {"marka": "Seat", "model": "Tarraco", "kasa": "SUV", "yakit": "Benzin", "motor_tipi": "1.5 TSI", "yil": "2018-2026", "ulke": "İspanya"},
    {"marka": "Cupra", "model": "Formentor", "kasa": "SUV", "yakit": "Benzin", "motor_tipi": "1.5 TSI", "yil": "2020-2026", "ulke": "İspanya"},
    {"marka": "Cupra", "model": "Leon", "kasa": "Hatchback", "yakit": "Benzin", "motor_tipi": "1.4 e-Hybrid", "yil": "2020-2026", "ulke": "İspanya"},
    {"marka": "Hyundai", "model": "Santa Fe", "kasa": "SUV", "yakit": "Dizel", "motor_tipi": "2.0 CRDi", "yil": "2012-2026", "ulke": "Güney Kore"},
    {"marka": "Hyundai", "model": "Kona", "kasa": "SUV", "yakit": "Elektrik", "motor_tipi": "e-Motor", "yil": "2017-2026", "ulke": "Güney Kore"},
    {"marka": "Hyundai", "model": "Ioniq 5", "kasa": "SUV", "yakit": "Elektrik", "motor_tipi": "e-Motor", "yil": "2021-2026", "ulke": "Güney Kore"},
    {"marka": "Kia", "model": "Sorento", "kasa": "SUV", "yakit": "Dizel", "motor_tipi": "2.0 CRDi", "yil": "2014-2026", "ulke": "Güney Kore"},
    {"marka": "Kia", "model": "Bongo", "kasa": "Ticari", "yakit": "Dizel", "motor_tipi": "2.5", "yil": "2004-2026", "ulke": "Güney Kore"},
    {"marka": "Kia", "model": "EV6", "kasa": "SUV", "yakit": "Elektrik", "motor_tipi": "e-Motor", "yil": "2021-2026", "ulke": "Güney Kore"},
    {"marka": "Peugeot", "model": "5008", "kasa": "SUV", "yakit": "Dizel", "motor_tipi": "1.5 BlueHDi", "yil": "2017-2026", "ulke": "Fransa"},
    {"marka": "Peugeot", "model": "408", "kasa": "SUV", "yakit": "Benzin", "motor_tipi": "1.2 PureTech", "yil": "2022-2026", "ulke": "Fransa"},
    {"marka": "Citroen", "model": "C4 X", "kasa": "Sedan", "yakit": "Benzin", "motor_tipi": "1.2 PureTech", "yil": "2022-2026", "ulke": "Fransa"},
    {"marka": "Citroen", "model": "C3 Picasso", "kasa": "MPV", "yakit": "Dizel", "motor_tipi": "1.6 HDi", "yil": "2009-2017", "ulke": "Fransa"},
    {"marka": "Opel", "model": "Grandland X", "kasa": "SUV", "yakit": "Dizel", "motor_tipi": "1.5 CDTI", "yil": "2017-2026", "ulke": "Almanya"},
    {"marka": "Opel", "model": "Combo", "kasa": "Ticari", "yakit": "Dizel", "motor_tipi": "1.5 BlueHDi", "yil": "2018-2026", "ulke": "Almanya"},
    {"marka": "Opel", "model": "Vectra", "kasa": "Sedan", "yakit": "Benzin", "motor_tipi": "1.6", "yil": "1995-2008", "ulke": "Almanya"},
    {"marka": "Toyota", "model": "Rav4", "kasa": "SUV", "yakit": "Hibrit", "motor_tipi": "2.5", "yil": "2018-2026", "ulke": "Japonya"},
    {"marka": "Toyota", "model": "Land Cruiser", "kasa": "SUV", "yakit": "Dizel", "motor_tipi": "2.8 D-4D", "yil": "2009-2026", "ulke": "Japonya"},
    {"marka": "Nissan", "model": "Note", "kasa": "Hatchback", "yakit": "Benzin", "motor_tipi": "1.2", "yil": "2013-2020", "ulke": "Japonya"},
    {"marka": "Nissan", "model": "Almera", "kasa": "Sedan", "yakit": "Benzin", "motor_tipi": "1.5", "yil": "2000-2006", "ulke": "Japonya"},
    {"marka": "Ford", "model": "Kuga", "kasa": "SUV", "yakit": "Dizel", "motor_tipi": "1.5 EcoBlue", "yil": "2012-2026", "ulke": "Amerika"},
    {"marka": "Ford", "model": "C-Max", "kasa": "MPV", "yakit": "Dizel", "motor_tipi": "1.6 TDCi", "yil": "2010-2019", "ulke": "Amerika"},
    {"marka": "Chevrolet", "model": "Captiva", "kasa": "SUV", "yakit": "Dizel", "motor_tipi": "2.0 D", "yil": "2006-2018", "ulke": "Amerika"},
    {"marka": "Chevrolet", "model": "Spark", "kasa": "Hatchback", "yakit": "Benzin", "motor_tipi": "1.0", "yil": "2009-2015", "ulke": "Amerika"},
    {"marka": "Volkswagen", "model": "Touareg", "kasa": "SUV", "yakit": "Dizel", "motor_tipi": "3.0 V6 TDI", "yil": "2010-2026", "ulke": "Almanya"},
    {"marka": "Volkswagen", "model": "Arteon", "kasa": "Sedan", "yakit": "Dizel", "motor_tipi": "2.0 TDI", "yil": "2017-2026", "ulke": "Almanya"},
    {"marka": "Volkswagen", "model": "Scirocco", "kasa": "Coupe", "yakit": "Benzin", "motor_tipi": "1.4 TSI", "yil": "2008-2017", "ulke": "Almanya"},
    {"marka": "Volkswagen", "model": "Bora", "kasa": "Sedan", "yakit": "Benzin", "motor_tipi": "1.6", "yil": "1998-2005", "ulke": "Almanya"},
    {"marka": "Chery", "model": "Omoda 5", "kasa": "SUV", "yakit": "Benzin", "motor_tipi": "1.6 TGDI", "yil": "2022-2026", "ulke": "Çin"},
    {"marka": "Chery", "model": "Tiggo 7 Pro", "kasa": "SUV", "yakit": "Benzin", "motor_tipi": "1.6 TGDI", "yil": "2020-2026", "ulke": "Çin"},
    {"marka": "Chery", "model": "Tiggo 8 Pro", "kasa": "SUV", "yakit": "Benzin", "motor_tipi": "1.6 TGDI", "yil": "2020-2026", "ulke": "Çin"}
]

def gizli_arac_sec():
    return random.choice(araclar)

@app.route('/')
def ana_sayfa():
    if 'gizli_arac' not in session:
        session['gizli_arac'] = gizli_arac_sec()
    return render_template('index.html', araclar=araclar)

@app.route('/tahmin', methods=['POST'])
def tahmin_et():
    if 'gizli_arac' not in session:
        return jsonify({"hata": "Oyun oturumu bulunamadı. Lütfen sayfayı yenileyin."})

    veri = request.get_json()
    kullanici_tahmini = veri.get('tahmin', '').strip().lower()
    
    bulunan_arac = None
    for arac in araclar:
        tam_isim = f"{arac['marka']} {arac['model']}".strip().lower()
        if tam_isim == kullanici_tahmini:
            bulunan_arac = arac
            break
            
    if not bulunan_arac:
        return jsonify({"hata": "Bu araç listede bulunamadı!"})
        
    gizli = session['gizli_arac']
    yanit = {}
    kazandi = True
    
    kriterler = ["marka", "model", "kasa", "yakit", "motor_tipi", "yil", "ulke"]
    for kriter in kriterler:
        if bulunan_arac[kriter] == gizli[kriter]:
            durum = "dogru"
        else:
            durum = "yanlis"
            kazandi = False
            
        yanit[kriter] = {"deger": bulunan_arac[kriter], "durum": durum}
        
    yanit["kazandi"] = kazandi
    return jsonify(yanit)

@app.route('/sifirla', methods=['POST'])
def sifirla():
    session['gizli_arac'] = gizli_arac_sec()
    return jsonify({"durum": "basarili"})

if __name__ == '__main__':
    app.run(debug=True)