# -*- coding: utf-8 -*-
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext
import datetime
import os, time
import sys
import mysql.connector
from telegram import ParseMode
my_os = sys.platform

my_os = sys.platform
token = 'telegram bot token'
updater = Updater(token=token, use_context=True)

dispatcher = updater.dispatcher

import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def insert_visit(user, timestamp):
    query = "INSERT INTO visit(visit_uid,visit_datetime) " \
            "VALUES(%s,%s)"
    args = (user, timestamp)

    try:
        conn = mysql.connector.connect(host='127.0.0.1', database='visit',user='root',password='')
        cursor = conn.cursor()
        cursor.execute(query, args)

        conn.commit()
    finally:
        cursor.close()
        conn.close()

#Start the bot
def start(update, context: CallbackContext ) -> None:
    context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('Day Zero/dzbot/banner.jpg','rb'))
    user = update.message.from_user
    #context.bot.send_message(chat_id=update.effective_chat.id, text="Hi "+ user['first_name'] +"! Looking for a way to get to one of SIT's Campuses for your First Year Experience? Select any of the Campuses below to begin your journey now!")
    keyboard = [
        [
            InlineKeyboardButton("SIT@Dover", callback_data='1'),
            InlineKeyboardButton("SIT@NP Building", callback_data='2')
        ],
        [
            InlineKeyboardButton("SIT@NYP Building", callback_data='3'),
            InlineKeyboardButton("SIT@RP Building", callback_data='4'),
        ],
        [
            InlineKeyboardButton("SIT@SP Building", callback_data='5'),
            InlineKeyboardButton("SIT@TP Building", callback_data='6'),
        ]
    ]
    os.environ['TZ'] = 'Singapore'
    if my_os == "linux":
        time.tzset()
    timenow = datetime.datetime.now()
    insert_visit(user['username'],timenow)
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Hi "+ user['first_name'] +"! Looking for a way to get to one of SIT's Campuses for your First Year Experience? Select any of the Campuses below to begin your journey now!", reply_markup=reply_markup)

# to send FYE2021 link
def fye2021(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="<a href='https://firstyearexperience.singaporetech.edu.sg/Registration/Login'>First Year Experience 2021</a>",parse_mode=ParseMode.HTML)

########################################START########################################
def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()

    # This will define which button the user tapped on (from what you assigned to "callback_data". As I assigned them "1" and "2"):
    choice = query.data

    # Now u can define what choice ("callback_data") do what like this:
    # Dover
    if choice == '1':
        keyboard = [
            [
                InlineKeyboardButton("Yes", callback_data='1-0-0'),
            ],
            [
                InlineKeyboardButton("No, I have reached SIT@Dover", callback_data='0-1')
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.callback_query.message.reply_text("Are you finding directions to SIT@Dover?", reply_markup=reply_markup)

    elif choice == '1-0-0':
        keyboard = [
            [
                InlineKeyboardButton("Yes, it is!", callback_data='1-0-1'),
            ],
            [
                InlineKeyboardButton("No, it's not!", callback_data='1-0')
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.callback_query.message.reply_text("Is it currently raining in the area?", reply_markup=reply_markup)
    # Rainy day option - Dover
    elif choice == '1-0-1':
        keyboard = [
            [
                InlineKeyboardButton("Buona Vista MRT (CC 22/EW 21)", callback_data='1-0-1-1'),
            ],
            [
                InlineKeyboardButton("One-North MRT (CC 23)", callback_data='1-0-1-2')
            ],
            [
                InlineKeyboardButton("Bus Stops along AYE", callback_data='1-3')
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.callback_query.message.reply_text("Where are you coming from?", reply_markup=reply_markup)

    elif choice == '1-0-1-1':
        keyboard = [
            [
                InlineKeyboardButton("Bus 198 to Opp SIT@Dover (16091)", callback_data='1-1-1'),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.callback_query.message.reply_text("From Buona Vista MRT, take Exit D and proceed to Buona Vista Exit D (11369) for Bus 198.", reply_markup=reply_markup)

    elif choice == '1-0-1-2':
        keyboard = [
            [
                InlineKeyboardButton("Yes! I do!", callback_data='1-2'),
            ],
            [
                InlineKeyboardButton("No I do not.", callback_data='1-0-1-3'),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.callback_query.message.reply_text("Do you have an umbrella?", reply_markup=reply_markup)

    elif choice == '1-0-1-3':
        keyboard = [
            [
                InlineKeyboardButton("I have reached Buona Vista MRT", callback_data='1-0-1-1'),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.callback_query.message.reply_text("As there is no covered shelter from One-North, please take the Circle Line to Buona Vista.", reply_markup=reply_markup)

    elif choice == '1-0':
        keyboard = [
            [
                InlineKeyboardButton("Buona Vista MRT (CC 22/EW 21)", callback_data='1-1'),
            ],
            [
                InlineKeyboardButton("One-North MRT (CC 23)", callback_data='1-2')
            ],
            [
                InlineKeyboardButton("Bus Stops along AYE", callback_data='1-3')
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.callback_query.message.reply_text("Where are you coming from?", reply_markup=reply_markup)

    elif choice == '1-1':
        keyboard = [
            [
                InlineKeyboardButton("SHED: Bus 198 to Opp SIT@Dover (16091)", callback_data='1-1-1'),
            ],
            [
                InlineKeyboardButton("AP: Bus 74 or 196 to Opp Fairfield Meth Pri School (18119)", callback_data='1-1-2')
            ],
            [
                InlineKeyboardButton("Continue on Circle Line to one-north", callback_data='1-1-3')
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.callback_query.message.reply_text("From Buona Vista MRT, take Exit D and proceed to Buona Vista Exit D (11369) for buses or continue on the Circle Line to one north.", reply_markup=reply_markup)

    elif choice == '1-1-1':
        context.bot.send_message(chat_id=update.effective_chat.id, text="Alight at Bus Stop 16091 (opposite SIT Dover). Cross the overhead bridge and walk along the walkway to enter via the back gate. Ushers at SIT@Dover are here to guide you to continue your journey. ")
        context.bot.send_message(chat_id=update.effective_chat.id, text="Have a great First Year Experience!")

    elif choice == '1-1-2':
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('Day Zero/dzbot/dover/7.png','rb'))
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('Day Zero/dzbot/dover/8.png','rb'))
        keyboard = [
            [
                InlineKeyboardButton("Let's Continue", callback_data='1-1-2-1'),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.callback_query.message.reply_text("Alight at Bus Stop 18119 (opposite Fairfield Methodist Primary School). Follow the path and turn left at the red shelter. ", reply_markup=reply_markup)

    elif choice == '1-1-2-1':
        context.bot.send_message(chat_id=update.effective_chat.id, text="Follow the pathway and there will be ushers at the side gate to guide you to continue your journey.")
        context.bot.send_message(chat_id=update.effective_chat.id, text="Have a great First Year Experience!")

    elif choice == '1-2' or choice == '1-1-3':
        #context.bot.send_message(chat_id=update.effective_chat.id, text="At One North MRT, take Exit A, Ayer Rajah Ave. Head up the escalator to the street level and turn right.")
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('Day Zero/dzbot/dover/1.png','rb'))
        keyboard = [
            [
                InlineKeyboardButton("Let's Continue", callback_data='1-2-1'),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.callback_query.message.reply_text("At One North MRT, take Exit A, Ayer Rajah Ave. Head up the escalator to the street level and turn right.", reply_markup=reply_markup)

    elif choice == '1-2-1':
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('Day Zero/dzbot/dover/2.png','rb'))
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('Day Zero/dzbot/dover/3.png','rb'))
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('Day Zero/dzbot/dover/4.png','rb'))
        keyboard = [
            [
                InlineKeyboardButton("Let's Continue", callback_data='1-2-2'),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.callback_query.message.reply_text("Follow the walkway to the pedestrian crossing. You will see pass INSEAD on your right", reply_markup=reply_markup)

    elif choice == '1-2-2':
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('Day Zero/dzbot/dover/5.png','rb'))
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('Day Zero/dzbot/dover/6.png','rb'))
        keyboard = [
            [
                InlineKeyboardButton("Let's Continue", callback_data='1-2-3'),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.callback_query.message.reply_text("Cross the traffic junction to the opposite side after passing Fairfield Methodist Primary School and continue walking straight.", reply_markup=reply_markup)

    elif choice == '1-2-3':
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('Day Zero/dzbot/dover/7.png','rb'))
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('Day Zero/dzbot/dover/8.png','rb'))
        keyboard = [
            [
                InlineKeyboardButton("Let's Continue", callback_data='1-2-4'),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.callback_query.message.reply_text("Once at the opposite side off the road, follow the path and turn left at the red shelter", reply_markup=reply_markup)

    elif choice == '1-2-4':
        context.bot.send_message(chat_id=update.effective_chat.id, text="Follow the pathway and there will be ushers to guide you to continue your journey.")
        context.bot.send_message(chat_id=update.effective_chat.id, text="Have a great First Year Experience!")

    elif choice == '1-3':
        keyboard = [
            [
                InlineKeyboardButton("Opposite SIT@Dover (16091)", callback_data='1-3-1'),
            ],
            [
                InlineKeyboardButton("SIT@Dover (16099)", callback_data='1-3-2')
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.callback_query.message.reply_text("Alighting at...", reply_markup=reply_markup)

    elif choice == '1-3-1':
        context.bot.send_message(chat_id=update.effective_chat.id, text="Cross the overhead bridge and enter through the back gate. Ushers at SIT@Dover are here to guide you to continue your journey.")
        context.bot.send_message(chat_id=update.effective_chat.id, text="Have a great First Year Experience!")

    elif choice == '1-3-2':
        context.bot.send_message(chat_id=update.effective_chat.id, text="Enter through the back gate. Ushers at SIT@Dover are here to guide you to continue your journey.")
        context.bot.send_message(chat_id=update.effective_chat.id, text="Have a great First Year Experience!")

    # NP
    elif choice == '2':
        keyboard = [
            [
                InlineKeyboardButton("Clementi MRT Station (EW 23)", callback_data='2-1'),
            ],
            [
                InlineKeyboardButton("King Albert Park MRT (DT 6)", callback_data='2-2')
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.callback_query.message.reply_text("Where are you coming from?", reply_markup=reply_markup)

    elif choice == '2-1':
        keyboard = [
            [
                InlineKeyboardButton("Let's Continue!", callback_data='2-1-1'),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.callback_query.message.reply_text("From Clementi MRT, take Exit B, and proceed to Clementi Stn Exit B (17179) for Buses 52, 154 or 184.",reply_markup=reply_markup)

    elif choice == '2-2':
        keyboard = [
            [
                InlineKeyboardButton("Let's Continue!", callback_data='2-2-1'),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.callback_query.message.reply_text("From King Albert Part MRT, take Exit B, and proceed to King Albert Pk Stn (42051) for Buses 74, 151 or 154. ",reply_markup=reply_markup)

    elif choice == '2-2-1':
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('Day Zero/dzbot/np/1.jpg','rb'))
        keyboard = [
            [
                InlineKeyboardButton("Let's Continue!", callback_data='2-2-2'),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.callback_query.message.reply_text("Taking Bus 74, 151 or 154, take 3 stops, alighting at Bus Stop 12109 (Opp Ngee Ann Poly). Cross the overhead bridge.",reply_markup=reply_markup)

    elif choice == '2-2-2':
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('Day Zero/dzbot/np/2.jpg','rb'))
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('Day Zero/dzbot/np/3.jpg','rb'))
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('Day Zero/dzbot/np/4.jpg','rb'))
        keyboard = [
            [
                InlineKeyboardButton("Let's Continue!", callback_data='2-1-2'),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.callback_query.message.reply_text("Go down the stairs on the opposite side and continue straight to the bus stop. Ngee Ann Polytechnic’s TraceTogether Checkpoint will come into view.",reply_markup=reply_markup)

    elif choice == '2-1-1':
        #context.bot.send_message(chat_id=update.effective_chat.id, text="Continue on through the temperature screening station")
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('Day Zero/dzbot/np/4.jpg','rb'))
        keyboard = [
            [
                InlineKeyboardButton("Let's Continue!", callback_data='2-1-2'),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.callback_query.message.reply_text("Taking Bus 52, 154 or 184, take 9 stops, alighting at Bus Stop 12101 (Ngee Ann Poly).",reply_markup=reply_markup)

    elif choice == '2-1-2':
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('Day Zero/dzbot/np/5.jpg','rb'))
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('Day Zero/dzbot/np/6.jpg','rb'))
        #context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('Day Zero/dzbot/np/5.jpg','rb'))
        keyboard = [
            [
                InlineKeyboardButton("Let's Continue!", callback_data='2-1-3'),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.callback_query.message.reply_text("Walk through the TraceTogether Checkpoint and continue straight under the sheltered walkway.",reply_markup=reply_markup)

    elif choice == '2-1-3':
        #context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('Day Zero/dzbot/np/6.jpg','rb'))
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('Day Zero/dzbot/np/7.jpg','rb'))
        keyboard = [
            [
                InlineKeyboardButton("Let's Continue!", callback_data='2-1-4'),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.callback_query.message.reply_text("Turn left at the end of the walkway and continue walking straight.",reply_markup=reply_markup)

    elif choice == '2-1-4':
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('Day Zero/dzbot/np/8.jpg','rb'))
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('Day Zero/dzbot/np/9.jpg','rb'))
        #context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('Day Zero/dzbot/np/10.jpg','rb'))
        keyboard = [
            [
                InlineKeyboardButton("Let's Continue!", callback_data='2-1-5'),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.callback_query.message.reply_text("Cross the zebra crossing to the opposite side. Remember to watch for traffic!",reply_markup=reply_markup)

    elif choice == '2-1-5':
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('Day Zero/dzbot/np/10.jpg','rb'))
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('Day Zero/dzbot/np/11.jpg','rb'))
        #context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('Day Zero/dzbot/np/13.jpg','rb'))
        keyboard = [
            [
                InlineKeyboardButton("Let's Continue!", callback_data='2-1-6'),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.callback_query.message.reply_text("Walk up the slope. Blks 72 and 52 will be on your left and the Convention Centre on your right.",reply_markup=reply_markup)

    elif choice == '2-1-6':
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('Day Zero/dzbot/np/12.jpg','rb'))
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('Day Zero/dzbot/np/13.jpg','rb'))
        keyboard = [
            [
                InlineKeyboardButton("Let's Continue!", callback_data='2-1-7'),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.callback_query.message.reply_text("Walk past the School of Film & Media Studies on your left and cross the zebra crossing ahead.",reply_markup=reply_markup)

    elif choice == '2-1-7':
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('Day Zero/dzbot/np/14.jpg','rb'))
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('Day Zero/dzbot/np/15.jpg','rb'))
        keyboard = [
            [
                InlineKeyboardButton("Let's Continue!", callback_data='2-1-8'),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.callback_query.message.reply_text("Once across, walk straight down the slope and cross the zebra crossing ahead, back to the other side of the road.",reply_markup=reply_markup)

    elif choice == '2-1-8':
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('Day Zero/dzbot/np/16.jpg','rb'))
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('Day Zero/dzbot/np/17.jpg','rb'))
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('Day Zero/dzbot/np/18.jpg','rb'))
        keyboard = [
            [
                InlineKeyboardButton("Let's Continue!", callback_data='2-1-9'),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.callback_query.message.reply_text("Blk 46 will be on your left. Continue walking straight and following the bend towards the right.",reply_markup=reply_markup)

    elif choice == '2-1-9':
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('Day Zero/dzbot/np/19.jpg','rb'))
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('Day Zero/dzbot/np/20.jpg','rb'))
        context.bot.send_message(chat_id=update.effective_chat.id, text="Continue straight all the way. SIT@TP Building will be on your right. There will be ushers at SIT@TP Building to receive and guide you to the allocated classrooms.")
        context.bot.send_message(chat_id=update.effective_chat.id, text="Have a great First Year Experience!")

    # NYP
    elif choice == '3':
        keyboard = [
            [
                InlineKeyboardButton("Yio Chu Kang MRT (NS 15)", callback_data='3-1'),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.callback_query.message.reply_text("Where are you coming from?", reply_markup=reply_markup)

    elif choice == '3-1':
        #context.bot.send_message(chat_id=update.effective_chat.id, text="Turn Left upon exiting the MRT gantry and walk towards (Exit B) the direction of the bus interchange")
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('Day Zero/dzbot/nyp/1.jpg','rb'))
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('Day Zero/dzbot/nyp/2.jpg','rb'))
        keyboard = [
            [
                InlineKeyboardButton("Let's Continue!", callback_data='3-2'),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.callback_query.message.reply_text("Turn Left upon exiting the MRT gantry taking Exit B, and walk towards the direction of the bus parking.",reply_markup=reply_markup)

    elif choice == '3-2':
        #context.bot.send_message(chat_id=update.effective_chat.id, text="Follow the walkway and you will reach NYP. Head up the escalator.")
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('Day Zero/dzbot/nyp/3.jpg','rb'))
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('Day Zero/dzbot/nyp/4.jpg','rb'))
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('Day Zero/dzbot/nyp/5.jpg','rb'))
        keyboard = [
            [
                InlineKeyboardButton("Let's Continue!", callback_data='3-3'),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.callback_query.message.reply_text("Follow the walkway and you will reach NYP. Head up the escalator.",reply_markup=reply_markup)

    elif choice == '3-3':
        #context.bot.send_message(chat_id=update.effective_chat.id, text="Continue on through the temperature screening station")
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('Day Zero/dzbot/nyp/6.jpg','rb'))
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('Day Zero/dzbot/nyp/7.jpg','rb'))
        keyboard = [
            [
                InlineKeyboardButton("Let's Continue!", callback_data='3-4'),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.callback_query.message.reply_text("Continue on through the temperature screening station",reply_markup=reply_markup)

    elif choice == '3-4':
        #context.bot.send_message(chat_id=update.effective_chat.id, text="After exiting the temperature screening station, turn left and take the escalator.")
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('Day Zero/dzbot/nyp/8.jpg','rb')) #changes make to number 8 image
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('Day Zero/dzbot/nyp/9.jpg','rb'))
        keyboard = [
            [
                InlineKeyboardButton("Let's Continue!", callback_data='3-5'),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.callback_query.message.reply_text("After exiting the Tracetogether checkpoint, walk straight across the foyer and go up the escalator.",reply_markup=reply_markup)

    elif choice == '3-5':
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('Day Zero/dzbot/nyp/10.jpg','rb'))
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('Day Zero/dzbot/nyp/11.jpg','rb'))
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('Day Zero/dzbot/nyp/12.jpg','rb'))
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('Day Zero/dzbot/nyp/13.jpg','rb'))
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('Day Zero/dzbot/nyp/14.jpg','rb'))
        context.bot.send_message(chat_id=update.effective_chat.id, text="Turn right after going up and follow the walkway which will lead you to SIT@NYP, and there will be ushers to guide you to continue your journey.")
        context.bot.send_message(chat_id=update.effective_chat.id, text="Have a great First Year Experience!")


    # RP
    elif choice == '4':
        keyboard = [
            [
                InlineKeyboardButton("Yes", callback_data='4-0-0'),
            ],
            [
                InlineKeyboardButton("No, I have reached SIT@RP", callback_data='0-4'),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.callback_query.message.reply_text("Are you finding directions to SIT@RP?",reply_markup=reply_markup)

    elif choice == '4-0-0':
        keyboard = [
            [
                InlineKeyboardButton("Yes, it is!", callback_data='4-0-1'),
            ],
            [
                InlineKeyboardButton("No, it's not!", callback_data='4-0')
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.callback_query.message.reply_text("Is it currently raining in the area?", reply_markup=reply_markup)

    elif choice == '4-0-1':
        keyboard = [
            [
                InlineKeyboardButton("Let's Continue!", callback_data='4-0-2'),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.callback_query.message.reply_text("From Woodlands MRT (NS 9) proceed to the bus interchange. Then take Bus 169 and alight at Bus Stop B46269 (Republic Polytechnic)", reply_markup=reply_markup)

    elif choice == '4-0-2':
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('Day Zero/dzbot/rp/rain/1.jpg','rb'))
        #context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('Day Zero/dzbot/rp/rain/2.jpg','rb'))
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('Day Zero/dzbot/rp/rain/3.jpg','rb'))
        keyboard = [
            [
                InlineKeyboardButton("Let's Continue!", callback_data='4-0-3'),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.callback_query.message.reply_text("After alighting from the bus, follow the sheltered walkway towards the entrance of Republic Polytechnic. ", reply_markup=reply_markup)

    elif choice == '4-0-3':
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('Day Zero/dzbot/rp/rain/4.jpg','rb'))
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('Day Zero/dzbot/rp/rain/5.jpg','rb'))
        keyboard = [
            [
                InlineKeyboardButton("Let's Continue!", callback_data='4-0-4'),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.callback_query.message.reply_text("Continue walking straight, passing Cheers and Subway towards the temperature screening station.", reply_markup=reply_markup)

    elif choice == '4-0-4':
        #context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('Day Zero/dzbot/rp/rain/6.jpg','rb'))
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('Day Zero/dzbot/rp/rain/7.jpg','rb'))
        #context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('Day Zero/dzbot/rp/rain/8.jpg','rb'))
        keyboard = [
            [
                InlineKeyboardButton("Let's Continue!", callback_data='4-0-5'),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.callback_query.message.reply_text("After passing through the temperature screening station, keep left and go up the ramp/ stairs", reply_markup=reply_markup)

    elif choice == '4-0-5':
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('Day Zero/dzbot/rp/rain/8.jpg','rb'))
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('Day Zero/dzbot/rp/rain/9.jpg','rb'))
        #context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('Day Zero/dzbot/rp/rain/11.jpg','rb'))
        keyboard = [
            [
                InlineKeyboardButton("Let's Continue!", callback_data='4-0-6'),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.callback_query.message.reply_text("At the \"S E G\" blocks,turn right and go up the ramp/ stairs. ", reply_markup=reply_markup)

    elif choice == '4-0-6':
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('Day Zero/dzbot/rp/rain/10.jpg','rb'))
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('Day Zero/dzbot/rp/rain/11.jpg','rb'))
        keyboard = [
            [
                InlineKeyboardButton("Let's Continue!", callback_data='4-0-7'),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.callback_query.message.reply_text("Keep left and continue walking straight up the ramp/ stairs.", reply_markup=reply_markup)

    elif choice == '4-0-7':
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('Day Zero/dzbot/rp/rain/12.jpg','rb'))
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('Day Zero/dzbot/rp/rain/13.jpg','rb'))
        keyboard = [
            [
                InlineKeyboardButton("Let's Continue!", callback_data='4-0-8'),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.callback_query.message.reply_text("Turn left and exit at the temperature screening station, and walk straight to the building across the road. ", reply_markup=reply_markup)

    elif choice == '4-0-8':
        context.bot.send_message(chat_id=update.effective_chat.id, text="There will be ushers at SIT@RP building to receive and guide you to the allocated classrooms.")
        context.bot.send_message(chat_id=update.effective_chat.id, text="Have a great First Year Experience!")

    elif choice == '4-0':
        keyboard = [
            [
                InlineKeyboardButton("I’ve reached Woodlands MRT (NS9)", callback_data='4-1'),
            ],
            [
                InlineKeyboardButton("I’m still on the way!", callback_data='4-2'),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.callback_query.message.reply_text("We recommend starting your journey from Woodlands MRT (NS9)",reply_markup=reply_markup)

    elif choice == '4-2':
        keyboard = [
            [
                InlineKeyboardButton("Let's Continue!", callback_data='4-1'),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.callback_query.message.reply_text("Sure! Click Continue when you have reached!",reply_markup=reply_markup)

    elif choice == '4-1':
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('Day Zero/dzbot/rp/1.jpg','rb'))
        keyboard = [
            [
                InlineKeyboardButton("Let's Continue!", callback_data='4-1-1'),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.callback_query.message.reply_text("Proceed to the bus interchange and board Bus 903/903M at Berth B4.",reply_markup=reply_markup)

    elif choice == '4-1-1':
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('Day Zero/dzbot/rp/2.jpg','rb'))
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('Day Zero/dzbot/rp/3.jpg','rb'))
        keyboard = [
            [
                InlineKeyboardButton("Let's Continue!", callback_data='4-1-2'),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.callback_query.message.reply_text("Alight at Bus Stop 46301 (Progen Building) and cross the road towards Admiralty Park Playground.",reply_markup=reply_markup)

    elif choice == '4-1-2':
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('Day Zero/dzbot/rp/4.jpg','rb'))
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('Day Zero/dzbot/rp/5.jpg','rb'))
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('Day Zero/dzbot/rp/6.jpg','rb'))
        keyboard = [
            [
                InlineKeyboardButton("Let's Continue!", callback_data='4-1-3'),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.callback_query.message.reply_text("Walk through the park, going up the steps, and you will see SIT@RP straight ahead.",reply_markup=reply_markup)

    elif choice == '4-1-3':
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('Day Zero/dzbot/rp/7.jpg','rb'))
        context.bot.send_message(chat_id=update.effective_chat.id, text="Continue on and there will be ushers at SIT@RP building to guide you to the temperature screening station and allocated classroom.")
        context.bot.send_message(chat_id=update.effective_chat.id, text="Have a great First Year Experience!")

    elif choice == '5':
        keyboard = [
            [
                InlineKeyboardButton("MRT", callback_data='5-1-1'),
            ],
            [
                InlineKeyboardButton("Bus", callback_data='5-1-2'),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.callback_query.message.reply_text("We will start our journey from Dover MRT. Will you be coming by MRT or Bus?",reply_markup=reply_markup)

    elif choice == '5-1-1':
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('Day Zero/dzbot/sp/1.jpg','rb'))
        context.bot.send_message(chat_id=update.effective_chat.id, text="From Dover MRT (EW 22) turn left upon exiting the gantry.")
        keyboard = [
            [
                InlineKeyboardButton("Let's Continue!", callback_data='5-1'),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.callback_query.message.reply_text("Enter Singapore Polytechnic via the overhead sheltered walkway.",reply_markup=reply_markup)

    elif choice == '5-1-2':
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('Day Zero/dzbot/sp/2.jpg','rb'))
        context.bot.send_message(chat_id=update.effective_chat.id, text="Taking bus 14, 74, 105, 147, 166 or 185 alight at Bus Stop B19031 (Singapore Polytechnic) or Bus Stop B19039 (opposite Singapore Polytechnic).")
        keyboard = [
            [
                InlineKeyboardButton("Let's Continue!", callback_data='5-1'),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.callback_query.message.reply_text("Enter Singapore Polytechnic via the overhead sheltered walkway.",reply_markup=reply_markup)

    elif choice == '5-1':
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('Day Zero/dzbot/sp/3.jpg','rb'))
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('Day Zero/dzbot/sp/4.jpg','rb'))
        context.bot.send_message(chat_id=update.effective_chat.id, text="After exiting the temperature screening station, walk straight along the sheltered walkway. You will pass by the Convention Centre and Auditorium on your right.")
        keyboard = [
            [
                InlineKeyboardButton("Let's Continue!", callback_data='5-2'),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.callback_query.message.reply_text("Continue straight, pass Blk T16 and continue along the sheltered walkway.",reply_markup=reply_markup)

    elif choice == '5-2':
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('Day Zero/dzbot/sp/6.jpg','rb'))
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('Day Zero/dzbot/sp/7.jpg','rb'))
        keyboard = [
            [
                InlineKeyboardButton("Let's Continue!", callback_data='5-3'),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.callback_query.message.reply_text("Turn left at the end of the sheltered walkway, continue straight and turn left again after passing the food court.",reply_markup=reply_markup)

    elif choice == '5-3':
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('Day Zero/dzbot/sp/8.jpg','rb'))
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('Day Zero/dzbot/sp/9.jpg','rb'))
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('Day Zero/dzbot/sp/10.jpg','rb'))
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('Day Zero/dzbot/sp/11.jpg','rb'))
        keyboard = [
            [
                InlineKeyboardButton("Let's Continue!", callback_data='5-4'),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.callback_query.message.reply_text("Walk straight through the Sports Arena, take the staircase up, turn right at the lift lobby and continue the path towards SIT@SP building.",reply_markup=reply_markup)

    elif choice == '5-4':
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('Day Zero/dzbot/sp/12.jpg','rb'))
        context.bot.send_message(chat_id=update.effective_chat.id, text="There will be ushers at SIT@SP building to receive and guide you to temperature screening station and the allocated classrooms.")
        context.bot.send_message(chat_id=update.effective_chat.id, text="Have a great First Year Experience!")

    elif choice == '6':
        keyboard = [
            [
                InlineKeyboardButton("Tampines MRT (EW 2)", callback_data='6-0'),
            ],
            [
                InlineKeyboardButton("Tampines West MRT (DT 31)", callback_data='6-0-0')
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.callback_query.message.reply_text("Where are you coming from?", reply_markup=reply_markup)

    # For wet weather plan
    elif choice == '6-0':
        keyboard = [
            [
                InlineKeyboardButton("Yes, it is!", callback_data='6-1'),
            ],
            [
                InlineKeyboardButton("No, it's not!", callback_data='6-0-1')
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.callback_query.message.reply_text("Is it currently raining in the area?", reply_markup=reply_markup)

    elif choice == '6-0-0':
        keyboard = [
            [
                InlineKeyboardButton("Yes, it is!", callback_data='6-2'),
            ],
            [
                InlineKeyboardButton("No, it's not!", callback_data='6-0-1')
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.callback_query.message.reply_text("Is it currently raining in the area?", reply_markup=reply_markup)

    elif choice == '6-1':
        context.bot.send_message(chat_id=update.effective_chat.id, text="Take Bus 8, 23 or 69 from the Tampines Bus Interchange or Bus 129 at Tampines Concourse Bus Interchange.")
        #context.bot.send_message(chat_id=update.effective_chat.id, text="Alight at Bus Stop 75239 (Temasek Polytechnic), enter Temasek Polytechnic via the Auditorium entrance.")
        keyboard = [
            [
                InlineKeyboardButton("Let's Continue!", callback_data='6-1-1'),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.callback_query.message.reply_text("Alight at Bus Stop 75239 (Temasek Polytechnic), enter Temasek Polytechnic via the Auditorium entrance.",reply_markup=reply_markup)

    elif choice == '6-2':
        context.bot.send_message(chat_id=update.effective_chat.id, text="Take exit B and cross over to take Bus 8 or 23 from Bus Stop 75059 (Bef Tampines West Stn).")
        #context.bot.send_message(chat_id=update.effective_chat.id, text="Alight at Bus Stop 75239 (Temasek Polytechnic), enter Temasek Polytechnic via the Auditorium entrance.")
        keyboard = [
            [
                InlineKeyboardButton("Let's Continue!", callback_data='6-1-1'),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.callback_query.message.reply_text("Alight at Bus Stop 75239 (Temasek Polytechnic), enter Temasek Polytechnic via the Auditorium entrance.",reply_markup=reply_markup)

    elif choice == '6-1-1':
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('Day Zero/dzbot/tp/0.jpg','rb'))
        keyboard = [
            [
                InlineKeyboardButton("Let's Continue!", callback_data='6-1-2'),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.callback_query.message.reply_text("Follow the directional signages to the temperature screening station located in the Auditorium.",reply_markup=reply_markup)

    elif choice == '6-1-2':
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('Day Zero/dzbot/tp/11.jpg','rb'))
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('Day Zero/dzbot/tp/12.jpg','rb'))
        #context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('Day Zero/dzbot/tp/0.jpg','rb'))
        keyboard = [
            [
                InlineKeyboardButton("Let's Continue!", callback_data='6-1-3'),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.callback_query.message.reply_text("After exiting the TraceTogether checkpoint, continue walking straight and check in once more into Garden Fiesta. ",reply_markup=reply_markup)

    elif choice == '6-1-3':
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('Day Zero/dzbot/tp/1.jpg','rb'))
        keyboard = [
            [
                InlineKeyboardButton("Let's Continue!", callback_data='6-1-4'),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.callback_query.message.reply_text("Walk past McDonald’s and continue walking straight, exiting the Garden Fiesta.",reply_markup=reply_markup)

    elif choice == '6-1-4':
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('Day Zero/dzbot/tp/2.jpg','rb'))
        keyboard = [
            [
                InlineKeyboardButton("Let's Continue!", callback_data='6-1-5'),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.callback_query.message.reply_text("Turn left and continue walking straight under the shelter.",reply_markup=reply_markup)

    elif choice == '6-1-5':
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('Day Zero/dzbot/tp/3.jpg','rb'))
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('Day Zero/dzbot/tp/4.jpg','rb'))
        keyboard = [
            [
                InlineKeyboardButton("Let's Continue!", callback_data='6-1-6'),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.callback_query.message.reply_text("At this point, walk in between the stairs and the lift and continue on under the sheltered walkway. The SIT@TP Building will come into view.",reply_markup=reply_markup)

    elif choice == '6-1-6':
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('Day Zero/dzbot/tp/5.jpg','rb'))
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('Day Zero/dzbot/tp/6.jpg','rb'))
        context.bot.send_message(chat_id=update.effective_chat.id, text="Continue walking along the same path towards Blk 26B. At Blk 26B, turn right after the vending machine and take the staircase down to SIT@TP building.")
        context.bot.send_message(chat_id=update.effective_chat.id, text="There will be ushers at SIT@TP building to receive and guide you to the allocated classrooms.")
        context.bot.send_message(chat_id=update.effective_chat.id, text="Have a great First Year Experience!")

    elif choice == '6-0-1':
        context.bot.send_message(chat_id=update.effective_chat.id, text="Take Bus 8, 23 or 69 from the Tampines Bus Interchange or Bus 129 at Tampines Concourse Bus Interchange.")
        #context.bot.send_message(chat_id=update.effective_chat.id, text="Alight at Bus Stop 75239 (Temasek Polytechnic), enter Temasek Polytechnic via the Auditorium entrance.")
        keyboard = [
            [
                InlineKeyboardButton("Let's Continue!", callback_data='6-0-2'),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.callback_query.message.reply_text("Alight at Bus Stop 75239 (Temasek Polytechnic), enter Temasek Polytechnic via the Auditorium entrance.",reply_markup=reply_markup)

    elif choice == '6-0-2':
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('Day Zero/dzbot/tp/0.jpg','rb'))
        keyboard = [
            [
                InlineKeyboardButton("Let's Continue!", callback_data='6-0-3'),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.callback_query.message.reply_text("Follow the directional signages to the temperature screening station located in the Auditorium.",reply_markup=reply_markup)

    elif choice == '6-0-3':
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('Day Zero/dzbot/tp/11.jpg','rb'))
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('Day Zero/dzbot/tp/12.jpg','rb'))
        keyboard = [
            [
                InlineKeyboardButton("Let's Continue!", callback_data='6-0-4'),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.callback_query.message.reply_text("After exiting the TraceTogether checkpoint, continue walking straight and turn left through the corridor before the Garden Fiesta entrance.",reply_markup=reply_markup)

    elif choice == '6-0-4':
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('Day Zero/dzbot/tp/7.jpg','rb'))
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('Day Zero/dzbot/tp/8.jpg','rb'))
        keyboard = [
            [
                InlineKeyboardButton("Let's Continue!", callback_data='6-0-5'),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.callback_query.message.reply_text("Continue along the pathway behind the Garden Fiesta. The SIT@TP building will come into view.",reply_markup=reply_markup)

    elif choice == '6-0-5':
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('Day Zero/dzbot/tp/9.jpg','rb'))
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('Day Zero/dzbot/tp/10.jpg','rb'))
        context.bot.send_message(chat_id=update.effective_chat.id, text="Continue on straight by the side of Blk 26B. Turn left and you take the staircase down to SIT@TP Building. ")
        context.bot.send_message(chat_id=update.effective_chat.id, text="There will be ushers at SIT@TP building to receive and guide you to the allocated classrooms.")
        context.bot.send_message(chat_id=update.effective_chat.id, text="Have a great First Year Experience!")

    elif choice == '0-1':
        context.bot.send_message(chat_id=update.effective_chat.id, text="Have a blast at your First Year Experience at SIT@Dover!!")

    elif choice == '0-4':
        context.bot.send_message(chat_id=update.effective_chat.id, text="Have a blast at your First Year Experience at SIT@RP!!")

########################################END########################################

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)
query_handler = CallbackQueryHandler(button)
dispatcher.add_handler(query_handler)
fye2021_handler = CommandHandler('fye2021', fye2021)
dispatcher.add_handler(fye2021_handler)

updater.start_polling()
print("Bot started...")
time.sleep(2)
print("beep...beep..")
time.sleep(1)
print("Start using dude...")