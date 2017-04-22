import numpy as np
import cPickle as pickle
import hickle
import time
import os

def load_word_to_idx(data_path='./cocodata', split='train'):
    data_path = os.path.join(data_path, split)
    start_t = time.time()
    if split == 'train':
        with open(os.path.join(data_path, 'word_to_idx.pkl'), 'rb') as f:
            word = pickle.load(f)
    end_t = time.time()
    print "Elapse time: %.2f" %(end_t - start_t)
    return word

def load_word2idx(data_path='./cocodata', split='train'):
    data_path = os.path.join(data_path, split)
    start_t = time.time()
    if split == 'train':
        with open(os.path.join(data_path, 'word2idx.pkl'), 'rb') as f:
            word = pickle.load(f)
    end_t = time.time()
    print "Elapse time: %.2f" %(end_t - start_t)
    return word

def load_coco_data(data_path='./cocodata', split='train', part=''):
    data_path = os.path.join(data_path, split)
    start_t = time.time()
    data = {}
    if split == 'train':
        data['features'] = hickle.load(os.path.join(data_path, '%s.features_%s.hkl' % (split, part)))
        with open(os.path.join(data_path, '%s.file.names_%s.pkl' % (split, part)), 'rb') as f:
            data['file_names'] = pickle.load(f)
        with open(os.path.join(data_path, '%s.captions_%s.pkl' % (split, part)), 'rb') as f:
            data['captions'] = pickle.load(f)
        with open(os.path.join(data_path, '%s.image.idxs_%s.pkl' % (split, part)), 'rb') as f:
            data['image_idxs'] = pickle.load(f)
        with open(os.path.join(data_path, 'word_to_idx.pkl'), 'rb') as f:
            data['word_to_idx'] = pickle.load(f)
        '''
        for k, v in data.iteritems():
            if type(v) == np.ndarray:
                print k, type(v), v.shape, v.dtype
            else:
                print k, type(v), len(v)
        '''
    else:
        data['features'] = hickle.load(os.path.join(data_path, '%s.features.hkl' % split))
        with open(os.path.join(data_path, '%s.file.names.pkl' %split), 'rb') as f:
            data['file_names'] = pickle.load(f)
        with open(os.path.join(data_path, '%s.captions.pkl' %split), 'rb') as f:
            data['captions'] = pickle.load(f)
        with open(os.path.join(data_path, '%s.image.idxs.pkl' %split), 'rb') as f:
            data['image_idxs'] = pickle.load(f)
        for k, v in data.iteritems():
            if type(v) == np.ndarray:
                print k, type(v), v.shape, v.dtype
            else:
                print k, type(v), len(v)
    end_t = time.time()
    print "Elapse time: %.2f" %(end_t - start_t)
    return data

def decode_captions(captions, idx_to_word):
    # for i in idx_to_word.iteritems():
    #     print i
    if captions.ndim == 1:
        T = captions.shape[0]
        N = 1
    else:
        N, T = captions.shape

    decoded = []
    for i in range(N):
        words = []
        for t in range(T):
            if captions.ndim == 1:
                word = idx_to_word[captions[t]]
            else:
                word = idx_to_word[captions[i, t]]
            # if word == '<END>':
            #   words.append('END')
            #   break
            if word != '<NULL>':
                words.append(word)
        decoded.append(' '.join(words))
    return decoded

def decode_py_captions(captions, idx_to_word):

    N = len(captions)
    decoded = []
    for i in range(N):
        words = []
        T = len(captions[i])
        for t in range(T):
            word = idx_to_word[captions[i][t] + 3]
            if word != '<NULL>':
                words.append(word)
        decoded.append(' '.join(words))
    return decoded

def sample_coco_minibatch(data, batch_size):
    data_size = data['features'].shape[0]
    mask = np.random.choice(data_size, batch_size)
    features = data['features'][mask]
    file_names = data['file_names'][mask]
    return features, file_names

def write_bleu(scores, path, epoch):
    if epoch == 0:
        file_mode = 'w'
    else:
        file_mode = 'a'
    with open(os.path.join(path, 'val.bleu.scores.txt'), file_mode) as f:
        f.write('Epoch %d\n' %(epoch+1))
        f.write('Bleu_1: %f\n' %scores['Bleu_1'])
        f.write('Bleu_2: %f\n' %scores['Bleu_2'])
        f.write('Bleu_3: %f\n' %scores['Bleu_3'])  
        f.write('Bleu_4: %f\n' %scores['Bleu_4']) 
        f.write('METEOR: %f\n' %scores['METEOR'])  
        f.write('ROUGE_L: %f\n' %scores['ROUGE_L'])  
        f.write('CIDEr: %f\n\n' %scores['CIDEr'])

def load_pickle(path):
    with open(path, 'rb') as f:
        file = pickle.load(f)
        print ('Loaded %s..' %path)
        return file  

def save_pickle(data, path):
    with open(path, 'wb') as f:
        pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)
        print ('Saved %s..' %path)
