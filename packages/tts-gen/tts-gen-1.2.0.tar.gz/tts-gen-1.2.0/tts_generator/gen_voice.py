#coding: utf-8

import os.path
import requests
import json
from tqdm import tqdm
from tts_generator import __server_url__, __server_bridge_url__

def gen_gx_voice(texts, output_dir, server_url=None, voice_num=None, wav_type='all', tts_server_name='gx'):
    if not server_url:
        server_url = __server_url__
    server_synthesize_url = server_url + '/api/synthesize_multi'
    server_info_url = server_url + '/api/info'

    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    headers = {
            'User-Agent'         : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36',
            'Accept-Language'    : 'zh-CN,zh;q=0.9',
            #'Content-Type'       : 'application/json',
            }

    with requests.Session() as session:
        r = session.get(url=server_info_url, headers=headers, verify=False)
        info = json.loads(r.text)
        if wav_type == 'train':
            max_voice_num = info['max_train_voice_num']
        elif wav_type == 'test':
            max_voice_num = info['max_test_voice_num']
        else:
            max_voice_num = info['max_voice_num']
        if not voice_num:
            voice_num = max_voice_num
        total_voice_num = min(max_voice_num, voice_num)

        for text in texts:
            print('generate %s wavs ...' % text)

            text_dir = os.path.join(output_dir, text)
            if not os.path.exists(text_dir):
                os.mkdir(text_dir)

            if wav_type in ('train', 'test'):
                text_dir = os.path.join(text_dir, wav_type)
                if not os.path.exists(text_dir):
                    os.mkdir(text_dir)
                list_f_name = '%s_%s.list' % (text, wav_type)
                wav_dir = '%s/%s' % (text, wav_type)
            else:
                list_f_name = '%s.list' % text
                wav_dir = '%s' % text

            list_f_path = os.path.join(output_dir, list_f_name)
            list_f = open(list_f_path, "w")
            blk_voice_num = 10 # 分块传输
            for voice_index in tqdm(range(0, total_voice_num, blk_voice_num)):
                data = {
                    'text': text,
                    'voice_index': voice_index,
                    'voice_num': min(blk_voice_num, total_voice_num - voice_index),
                    'wav_type': wav_type,
                    }
                r = session.post(url=server_synthesize_url, data=data, headers=headers, verify=False)
                #print(r.content)
                #print(r.headers['Content-Type'])
                wav_split_map = json.loads(r.headers['Content-Type'])
                for k, v in wav_split_map.items():
                    begin, end = v[0], v[1]
                    with open('%s' % os.path.join(text_dir, k), 'wb') as f:
                        f.write(r.content[begin:end])
                    list_f.write('%s,%s\n' % (os.path.join(wav_dir, k), text))
                #print('content len:', len(r.content))
            list_f.close()


def gen_other_voice(texts, output_dir, bridge_server_url, voice_num, wav_type, tts_server_name):
    if not bridge_server_url:
        server_url = __server_bridge_url__
    server_synthesize_url = server_url + '/api/synthesize_multi'
    server_info_url = server_url + '/api/info'

    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    headers = {
            'User-Agent'         : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36',
            'Accept-Language'    : 'zh-CN,zh;q=0.9',
            #'Content-Type'       : 'application/json',
            }

    with requests.Session() as session:
        r = session.get(url=server_info_url, headers=headers, params={'platform':tts_server_name}, verify=False)
        info = json.loads(r.text)
        max_voice_num = info['max_voice_num']
        print(max_voice_num)
        if not voice_num:
            voice_num = max_voice_num
        total_voice_num = min(max_voice_num, voice_num)

        for text in texts:
            print('generate %s wavs ...' % text)

            text_dir = os.path.join(output_dir, text)
            if not os.path.exists(text_dir):
                os.mkdir(text_dir)

            list_f_name = '%s.list' % text
            wav_dir = '%s' % text
            list_f_path = os.path.join(output_dir, list_f_name)
            list_f = open(list_f_path, "w")
            blk_voice_num = 10 # 分块传输
            for voice_index in tqdm(range(0, total_voice_num, blk_voice_num)):
                data = {
                    'text': text,
                    'voice_index': voice_index,
                    'voice_num': min(blk_voice_num, total_voice_num - voice_index),
                    'wav_type': wav_type,
                    'platform': tts_server_name,
                    }
                r = session.post(url=server_synthesize_url, data=data, headers=headers, verify=False)
                #print(r.content)
                #print(r.headers['Content-Type'])
                wav_split_map = json.loads(r.headers['Content-Type'])
                for k, v in wav_split_map.items():
                    begin, end = v[0], v[1]
                    with open('%s' % os.path.join(text_dir, k), 'wb') as f:
                        f.write(r.content[begin:end])
                    list_f.write('%s,%s\n' % (os.path.join(wav_dir, k), text))
                #print('content len:', len(r.content))
            list_f.close()



def gen_voice(texts, output_dir, server_url=None, bridge_server_url=None, voice_num=None, wav_type='all', tts_server_name='gx'):
    if tts_server_name == 'gx':
        return gen_gx_voice(texts, output_dir, server_url, voice_num, wav_type)
    else:
        return gen_other_voice(texts, output_dir, bridge_server_url, voice_num, wav_type, tts_server_name)


if __name__ == '__main__':
    texts = []
    texts.append('你好小爱')
    texts.append('天猫精灵')
    #gen_voice(texts, './wavs')
    gen_voice(texts, './wavs', tts_server_name='aliyun')
    #gen_voice(texts, './wavs', tts_server_name='mobvoi')
    #gen_voice(texts, './aliyun_wavs', tts_server_name='aliyun')
    #gen_voice(texts, './xfyun_wavs', tts_server_name='xfyun')

