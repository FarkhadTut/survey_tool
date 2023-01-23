from math import prod
from tg.bot import RETURN_BUTTON, Bot, NEXT_BUTTON
from configs.config import TOKEN
from database.fetcher import poll, questions, answers
import sys
from typing import Dict




def poll_to_dict(poll_, questions_, answers_):
    langs = ['ru', 'uz']
    poll_dicts = []
    mask = poll_['status'] == 1 #chosing active poll, can be chosen by user in the future
    active_polls = poll_[mask]
    
    for j in active_polls.index:
        poll = active_polls.iloc[j]
        active_poll_id = poll['id']
        # poll = poll_[mask]
        poll_dict = {}
        poll_dict['data'] = {}
        for lang in langs:
            # if lang == 'ru':
            #     continue
            poll_dict['data'][lang] = {}
            mask = questions_['poll_id'] == active_poll_id
            questions = questions_[mask]
            questions.reset_index(drop=True, inplace=True)
            for i in questions.index:
                poll_dict['data'][lang][i] = {}
                question = questions[lang].iloc[i]
                question_id = questions['id'].iloc[i]
                type_ = questions['type'].iloc[i]
                finish = questions['finish'].iloc[i]
                mask = answers_['question_id'] == questions['id'].iloc[i]
                answers = answers_[mask]
                poll_dict['data'][lang][i][f'question'] = question
                poll_dict['data'][lang][i][f'type'] = type_
                poll_dict['data'][lang][i][f'finish'] = finish
                poll_dict['data'][lang][i][f'question_id'] = question_id
                poll_dict['data'][lang][i][f'answers'] = []
                answers.reset_index(drop=True, inplace=True)
                if type_ == 'multiple':
                    poll_dict['data'][lang][i][f'answers'].append([NEXT_BUTTON, next_question, 0])

                
                
                for k, index in enumerate(answers.index):
                    
                    
                    answer = answers[lang].iloc[index]
                    answer_id = answers['id'].iloc[index]
                    next_question = answers['next_question'].iloc[index]
                    if k == 0:
                        poll_dict['data'][lang][i][f'answers'].append([RETURN_BUTTON, next_question, -1])
                    poll_dict['data'][lang][i][f'answers'].append([answer, next_question, answer_id])
                    
        
        poll_dict['id'] = active_poll_id
        poll_dict['name'] = poll['name']
        poll_dicts.append(poll_dict)
    return poll_dicts


poll_dicts = poll_to_dict(poll, questions, answers)
# add_return_button(poll_to_dict)

bot = Bot(TOKEN, poll_dicts)
states = bot.define_states(list(range(0,999)), bot.respond)
conv_handler = bot.poll_conv_handler(states=states, entry='start', fallback='cancel')
bot.add_handler(conv_handler, group=0)

states = bot.define_states(list(range(0,999)), bot.settings_respond)
conv_handler = bot.choose_conv_handler(states=states, entry='choose', fallback='cancel_choose')
bot.add_handler(conv_handler, group=1)


bot.run()