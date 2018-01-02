# Stepwise Intructions for developing the Kannada ASR.

The instructions that follow will guide you through every step of developing a Kannada speech to text system for isolated word recognition. Get the entire code and dataset from the following link:
www.ajayhalthor.com/projects/code.zip

This project uses Python 2.7.11. for file manipulation operations. The files are already present in main directories in the form. 			

	`<subword>_<sample_rate>K`
    
Subword is either Syllable (syl) or Triphone (tri). For example:
- _syl_16K_ is the execution of Syllable based ASR for the dictionary of 750 words at the sample rate 16kHz. 
- _syl_22K_ is the execution of Syllable based ASR for the dictionary of 750 words at the sample rate 22kHz. 
- _tri_16K_ is the triphone based ASR for a 750 word dictionary where the sample rate is 16 kHz. 
- _tri_22K_ is the triphone based ASR for a 750 word dictionary where the sample rate is 22.05 kHz. 

Since the monophone analysis is a part of both Syllable and Triphone based analysis, the corresponding monophone Kannada ASR is performed in each directory.

For small sized dictionaries of 500 words, the required files are in the "small_subword" directory.i.e _small_syl_ or _small_tri_.

Note that the sample files provided are tuned to my voice. This is **speaker dependent** ASR. If you wish to train the ASR for your voice, just follow the steps below using your own voice samples for training.  We will discuss the construction of _syl_16K_ for the sample instructions. Replace the sample rates and subwords for the ASR you develop.

## Some Important Files and Folders
**/bin** : julia files for internal file processing.

**/python_scripts** : python files for audio and file processing

**/samples** : Initially recorded training data

**/samples_converted** : Converted files from /samples

**/recorded_test_samples** : Initially recorded testing data

**/test_samples** : Converted files from _/recorded_test_samples_

**/tokens** : files of tokens in Kannada that is used by the python scripts

**prompts.txt** : Text Transcription of training data

**monophones0** : Initial phones of the Kannada Language

**monophones1** : Same as monophones0 with a short pause phone `sp`.

**incorrect_words** : For every ASR, the performance is stored in this file. Note there are multiple occurrences of this file. Some examples are shown below.

- `syl_16K/small_syl/long/syl/incorrect_words.txt` shows the results of the Syllable ASR on the longest 500 word dictionary. 

- `syl_16K/small_syl/incorrect_words.txt` shows the results of the Syllable ASR on the 750 word dictionary.

- `syl_16K/small_syl/incorrect_words_mono.txt` shows the results of the Monophone ASR on the 750 word dictionary.


#### 1. Create Dataset
- Record Samples Sentences in the `samples` directory. There are 100 such samples. Export them as WAV files with sample rate 44.1KHz. Be sure to choose a high sample rate as WAV files can be downsampled.

- `prompts.txt` holds the transcription of those 100 sentences.

#### 2. Create wordlist 
The `wlist` consists of all unique words in `prompts.txt`. Create this word list with the following command using `bin/prompts2wlist.jl`.

	$ julia bin/prompts2wlist.jl prompts.txt wlist


#### 3. Create Monophone Pronunciation Dictionary.
- `monophones0` has all Kannada phones 46 with a silent phone `sil`.
- `monophones1` has an additional short pause `sp` phone.

The dictionary `dict` is constructed for every word in `wlist` using the following command.
	
    $ python python_scripts/create_dict.py

#### 4. Word & Phone Transcription 
Create the Word Level Transcription File `words.mlf` from `prompts.txt` by separating each word line by line using `bin/prompts2mlf.jl`.

	$ julia bin/prompts2mlf.jl prompts.txt words.mlf

Now, create a new file where every phone is on a new line using `mkphones0.led` and `HLed` with the following command. You can use the `mkphones0.led` for new projects without changes.

	$ HLEd -A -D -T 1 -l '*' -d dict -i phones0.mlf mkphones0.led words.mlf 

The phone level transcription is stored in `phones0.mlf`. We include short pause phones `sp` after after every word with the following command using `mkphones1.led`.You can use the `mkphones1.led` for new projects without changes.

	$ HLEd -A -D -T 1 -l '*' -d dict -i phones1.mlf mkphones1.led words.mlf 

This creates the required file with name `phones1.mlf`.

*__NOTE__ : Contents of `phones0.mlf` and `phones1.mlf` may not contain actual Kannada characters, but their **Octal Encding** instead. This is perfectly fine. We will convert it to Kannada Script at a later stage.*

#### 5. Convert Audio Data
The recorded sentences used for training in the `samples` directory should be converted to PCM , mono-channel WAV files with a custom sample rate. This is accomplished following these 3 steps:
- Create an empty directory `samples_converted`.
- Open `convert_pcm_mono.py` and change the source and destination directory variable to `samples` and `samples_converted` respectively.
- Then execute the following python file

		$ python python_scripts/convert_pcm_mono.py

`samples_converted` will be our output WAV data.


#### 6. Create Training Paths
We need to create a file with all paths to the MFCC files. Execute the following command to create `codetrain.scp`.

	$ python python_scripts/create_codetrain_scp.py
    
`codetrain.scp` file is created. It contains a list of audio files on the left and corrusponding MFCC files on the right. We will generate these MFCC files in the next step.

#### 7. Create MFCC Vectors
Create directory `train/mfcc` and specify a configuration file for the MFCCs to be created in `wav_config` (This file is provided). Execute the following command:

	HCopy -A -D -T 1 -C wav_config -S codetrain.scp 

This creates MFCCs for every sample in the `train/mfcc` directory.

*__TIP__: Check the format of the MFCC feature vectors with HList.*

#### 8. Create `train.scp`
Create a `train.scp` file which only contains the paths to the traning files. This is done by extracting the 2nd column of `codetrain.scp`. Hence we execute the following command to create `train.scp`.
	
	$ python python_scripts/create_train_scp.py


#### 9. HMM Prototype Initialization
Initialize the HMM Prototype in the `proto` file and define a configuration file `config`. We provide both files. 


#### 10. Create initial `hmm` folder
Create an empty folder called `hmm0` and execute the `HTK` command `HCompV` as shown.
	
	$ HCompV -A -D -T 1 -C config -f 0.01 -m -S train.scp -M hmm0 proto

This creates the files `proto` and `vfloors` in the `hmm0` directory.


#### 11. Create initial `hmmdefs` file
Copy `monophones0` into the `hmm0` directory. Then create the hmmdefs file by getting into the `hmm0` directory and executing `create_hmmdefs.py`. Note this python file is not with the others in `python_scripts`.

	$ cd hmm0
	$ python create_hmmdefs.py

`hmmdefs` initializes all HMMs for every monophone with parameters similar to the `proto` file.


#### 12. Create initial `macros` file
Create a `macros` file by copying the first 3 lines of `proto` followed by the entire content of `vfloors`. The resulting file (for syl_16K) looks something like this:
```
~o
<STREAMINFO> 1 25
<VECSIZE> 25<NULLD><MFCC_D_N_Z_0><DIAGC>
~v varFloor1
<Variance> 25
6.337364e-01 4.811290e-01 5.212138e-01 6.297672e-01 6.965734e-01 5.789758e-01 6.618909e-01 5.280533e-01 5.847340e-01 4.740644e-01 4.464558e-01 3.826577e-01 2.126088e-02 2.240220e-02 2.076481e-02 2.780402e-02 2.979447e-02 3.084975e-02 3.029560e-02 2.887547e-02 2.790046e-02 2.530517e-02 2.348650e-02 2.055844e-02 2.977529e-02
```


#### 13. Create `hmm1` ~ `hmm15` directories
Go to parent directory and create 15 folders and name them `hmm0`, `hmm1` till `hmm15`.

	$ cd ..

#### 14. First Round Parameter Reestimation
Start Reestimation of Monophones using the following commands consecutively.

	$ HERest -A -D -T 1 -C config -I phones0.mlf -t 250.0 150.0 1000.0 -S train.scp -H hmm0/macros -H hmm0/hmmdefs -M hmm1 monophones0
    
	$ HERest -A -D -T 1 -C config -I phones0.mlf -t 250.0 150.0 1000.0 -S train.scp -H hmm1/macros -H hmm1/hmmdefs -M hmm2 monophones0
    
	$ HERest -A -D -T 1 -C config -I phones0.mlf -t 250.0 150.0 1000.0 -S train.scp -H hmm2/macros -H hmm2/hmmdefs -M hmm3 monophones0

You may get warnings about the use of 3 phones : ೠ(rū), ಝ್(jha),  and ಞ್(ña). This is because they rarely occur in the dataset and in the langauge in general. Although ideally there should not be warnings, we continue due to dearth of these phones in contextual sentences. Do not worry. It does not affect our analysis. 

#### 15. Create `sp` model
Copy contents of `hmm3` to `hmm4`. We add an HMM model for the short pause `sp` by copying the model for `sil`. The following changes are made to the new `sp` model.
- Since this only has a single emitting state remove the states 2 and 4 
- rename state 3 to state 2.
- the number of states reduces from 5 to 3. the first and last states are dummy states. Change `<NUMSTATES>` to 3.
- The transition matrix now is size `3 x 3`. Specify this dimension of the square matrix in `<TRANSP>` and use the probability matrix as shown.
```
0.0 1.0 0.0
0.0 0.9 0.1
0.0 0.0 0.0
```

The final model that is added to `hmm4/hmmdefs` should look something like this : 
```
~h "sp"
<BEGINHMM>
<NUMSTATES> 3
<STATE> 2
<MEAN> 25
 -7.302736e+00 4.144721e+00 -7.887374e-01 3.412668e+00 6.260005e+00 4.898931e+00 3.274674e+00 6.217006e+00 3.928748e+00 5.020547e+00 4.479059e+00 3.938468e+00 5.479546e-04 8.916539e-04 2.116692e-03 4.812353e-03 6.664995e-03 3.580635e-03 -1.046601e-03 -2.260857e-03 -4.903398e-03 -4.901459e-03 -9.201490e-04 -6.301282e-04 3.075077e-04
<VARIANCE> 25
 2.974267e+00 2.598557e+00 3.760918e+00 4.748853e+00 6.819769e+00 7.160915e+00 8.311834e+00 1.040073e+01 9.594397e+00 9.785214e+00 9.586113e+00 8.758175e+00 7.504711e-02 1.671045e-01 2.675951e-01 3.924670e-01 5.473407e-01 6.561234e-01 7.859427e-01 8.902057e-01 9.422729e-01 9.954396e-01 9.286773e-01 8.653579e-01 3.693233e-02
<GCONST> 5.659990e+01
<TRANSP> 3
0.0 1.0 0.0
0.0 0.9 0.1
0.0 0.0 0.0
<ENDHMM>
```
Tie the center states of `sil` and `sp` and create a new set of models in `hmm5` with the following command. Remember to copy `sil.hed` to your directory. There is no need to change it's contents.

	$ HHEd -A -D -T 1 -H hmm4/macros -H hmm4/hmmdefs -M hmm5 sil.hed monophones1

#### 16. Second Round Parameter Reestimation
Perform Reestimation to incorperate updates.

	$ HERest -A -D -T 1 -C config  -I phones1.mlf -t 250.0 150.0 3000.0 -S train.scp -H hmm5/macros -H  hmm5/hmmdefs -M hmm6 monophones1
    
	$ HERest -A -D -T 1 -C config  -I phones1.mlf -t 250.0 150.0 3000.0 -S train.scp -H hmm6/macros -H hmm6/hmmdefs -M hmm7 monophones1

#### 17. Alignment of Speech and Text
We use `HVite` to align phone transcription and speech.

	$ HVite -A -D -T 1 -l '*' -o SWT -b SENT-END -C config -H hmm7/macros -H hmm7/hmmdefs -i aligned.mlf -m -t 250.0 150.0 1000.0 -y lab -a -I words.mlf -S train.scp dict monophones1> HVite_log

The `aligned.mlf` is created and performs this mapping.

#### 18. Third Round Round Parameter Reestimation
Perform Reestimation once again to incorperate updates.

	$ HERest -A -D -T 1 -C config -I aligned.mlf -t 250.0 150.0 3000.0 -S train.scp -H hmm7/macros -H hmm7/hmmdefs -M hmm8 monophones1 
    
	$ HERest -A -D -T 1 -C config -I aligned.mlf -t 250.0 150.0 3000.0 -S train.scp -H hmm8/macros -H hmm8/hmmdefs -M hmm9 monophones1


This step generates the final set of HMMs in `hmm9` which is used for monophone analysis. However, we contonue with either Syllable Modeling or Triphone Modeling.

## Monophone Modeling
#### 19. Decode Octal File `hmmdefs`
`hmm9/hmmdefs` will be used with `monophones1` for monophone based speech to text synthesis. However, notice that `hmm9/hmmdefs` is Octal encoded. Open the python interpreter. Assign the contents of `hmmdefs` to this variable and print it on the screen. The text will be decoded into Kannada script. Now copy this printed result into a new file `hmm9/hmmdefs_kn`.

`hmm9/hmmdefs_kn` will be used instead of `hmm9/hmmdefs` for monophone based ASR. You could go to the _Testing and Evaluation_ phase at this point to see your progrees, or continue further for Triphone or Syllable modeling.


## Trihpone Modeling
#### 19. Create Triphone Pronunciation Dictionary
Triphone `dict-tri` is created by executing :

	$ python python_scripts/create_dict_tri.py
    
Now **go to step 21**.

## Syllable Modeling

#### 19. Create a Syllable Pronunciation Dictionary

`create_dict_syl.py` is used to create the syllable dictionary `dict_syl.txt` and a syllable list `syllables1`. 

	$ python python_scripts/create_dict_syl.py

The syllable dictionary has 3 fields for every word entry much like the monophone dictionary: internal representation, external representation and syllable sequence. 


#### 20. Convert Syllables to Triphone representation

Execute `create_dict_syl_tri.py` to get the triphone sequence for every syllable. Note, this is not the same as triphone ASR where we obtain triphones for words. 

	$ python python_scripts/create_dict_syl_tri.py

Triphone representation of syllables is used because our decoder, HVite, can only work with triphones inherently. The resulting dictionary is `dict-tri`. All syllables (of triphones) encountered are stored in `fulllist0`


#### 21. Fix `fullist0`

`fulllist0` consists of 554 unique syllables used across the training samples, including short pause `sp` and silence `sil`. We want to append any additional entries in the `monophones0` file that may have been left out of the samples. 

	ಘ್ (gh)
	ಛ್ (ch)
	ಝ್ (jh)
	ಞ್ (ñ)
	ಠ್ (ṭh)
	ಢ್ (ḍh)
	ಥ್ (th)
	ಭ್ (b)
	ೠ (ru)

These are appended to `fulllist0` and the entire list is written to a new file `fulllist`. This is done with the following command.

	$ julia bin/fixfulllist.jl fulllist0 monophones0 fulllist


#### 22. Create subword transcriptions (using triphones)
Execute `create_wintri.py` create the syllable transcription of training sample sentences `prompts.txt`.

	$ python python_scripts/create_wintri.py

This creates a master label file `wintri.mlf` with syllabic transcriptions using triphones.

#### 23. Tie HMMs 

Create `mktri.hed` to tie HMMs together so they share the same parameters by executing the following commands.

	$ julia bin/mktrihed.jl monophones1 triphones1 mktri.hed

	$ HHEd -A -D -T 1 -H hmm9/macros -H hmm9/hmmdefs -M hmm10 mktri.hed monophones1 

#### 24. Fourth Round of Parameter Reestimation:
Perform Reestimation once again to incorperate updates.	

	$ HERest  -A -D -T 1 -C config -I wintri.mlf -t 250.0 150.0 3000.0 -S train.scp -H hmm10/macros -H hmm10/hmmdefs -M hmm11 triphones1 
        
	$ HERest  -A -D -T 1 -C config -I wintri.mlf -t 250.0 150.0 3000.0 -s stats -S train.scp -H hmm11/macros -H hmm11/hmmdefs -M hmm12 triphones1 
	
Warnings may occur due to limited Syllable samples. We solve this by tying HMMs for different syllables.


#### 25. Construction of descision tree

Based on contextual questions for the Kannada langauge specified in `tree1.hed`, a decision tree is created. This is used to tie triphones (of syllables) with similar context, reducing the number of HMM models.

Copy contents to a file `tree.hed`.

	$ cat tree1.hed > tree.hed

Execute `mkclscript.jl` to append state clusters at the end of the newly created `tree.hed`.

	$ julia bin/mkclscript.jl monophones0 tree.hed

#### 26. Create `tiedlist`

	$ HHEd -A -D -T 1 -H hmm12/macros -H hmm12/hmmdefs -M hmm13 tree.hed triphones1 

You may get an error : 

	FindProtoModel: no proto for ೠ in hSet
    
   This appears because ೠ(ru)is a part of our monophones file, yet there are no examples using this character. To get rid of this error, remove ೠ from `fulllist` near the last line of the file and execute this HHed command once more. 
   
	$ HHEd -A -D -T 1 -H hmm12/macros -H hmm12/hmmdefs -M hmm13 tree.hed triphones1 
    
This creates a `tiedlist` file which has syllables that have the same pronunciation in different context on a line.

#### 27. Final Round Parameter Reestimation
Perform re-estimation 2 more times to generate the final hmm definitions in `hmm15/hmmdefs`.

	$ HERest -A -D -T 1 -T 1 -C config -I wintri.mlf  -t 250.0 150.0 3000.0 -S train.scp -H hmm13/macros -H hmm13/hmmdefs -M hmm14 tiedlist
        
	$ HERest -A -D -T 1 -T 1 -C config -I wintri.mlf  -t 250.0 150.0 3000.0 -S train.scp -H hmm14/macros -H hmm14/hmmdefs -M hmm15 tiedlist


#### 28. Get Kannada Text

`hmm15/hmmdefs` and `tiedlist` are octal encoded. Convert them to Kannada text by opening the python interpreter in the terminal, assigning the entire file contents to a variable and subsequently printing the variable. Consider copying the contents of `tiedlist` into variable `a` as shown. 

		$ python
		>>> a = """
		... \340\262\206+\340\262\256\340\263\215
		...\340\262\247\340\263\215-\340\262\205
		...\340\262\247\340\263\215-\340\262\206
		...\340\262\247\340\263\215-\340\262\207
		.
		.
		.
		"""
		>>>
		>>> print a
		ಆ+ಮ್
		ಧ್-ಅ
		ಧ್-ಆ
		ಧ್-ಇ
		.
		.
		.
		>>>

Copy result of `print a` and paste it into `tiedlist_kn`. Repeat the same for `hmm15/hmmdef`. Assigning it's contents to a variable `b`, copy the result of  `print b` into `hmm15/hmmdefs_kn`. 

### Testing and Evaluation
---

#### 29. Convert Testing Data
We need to create our testing files. Recorded Voice Samples for every word are stored as WAV files in `recorded_test_samples`. They are recorded at a sample rate 44.1 kHz. 

Create an empty directory `test_samples`. Open `convert_pcm_mono.py` and change the source and destination directory variable to `recorded_test_samples` and `test_samples` respectively. Then execute

	$ python python_scripts/convert_pcm_mono.py

`test_samples` will consist of our Mono-channel PCM WAV test files.


#### 30. Create Grammar File

The grammar of recognized sentences is defined in `grammar`. For the problem of isolated word recognition, a "sentence" is a "word" flanked by 2 slience phones. 

	$ HParse grammar wdnet

This will create `wdnet`.

#### 31. Create Test Reference

The test reference file `testref.mlf` has a list of testing files and corresponding word to be recognized. It is created using `create_testref_mlf.py` by executing the following command.

	$ python python_scripts/create_testref_mlf.py

In `testref.mlf`, you may need to replace `SENT-START` and `SENT-END` with `sil`. A sample part of the file should look like the following:

    "*/ಅಗಾಧ_.lab"
    sil
    ಅಗಾಧ
    sil
    .
    "*/ಅತಿ_.lab"
    sil
    ಅತಿ
    sil
    .
    "*/ಅತ್ಯದ್ಭುತ_.lab"
    sil
    ಅತ್ಯದ್ಭುತ
    sil
    .
    "*/ಅಥವಾ_.lab"
    sil
    ಅಥವಾ
    sil
    .
    "*/ಅದರ_.lab"
    sil
    ಅದರ
    sil
    .
    "*/ಅದು_.lab"
    sil
    ಅದು
    sil
    .
    "*/ಅದೇ_.lab"
    sil
    ಅದೇ
    sil


#### 32. HVite Configuration

Our decoder HVite needs to be configured to recognize different sample rates. The only attribute that needs to be change in the configuration file `config_Hvite` is `SOURCERATE`. This unit is in `100 ns`. In  _syl_16K_ , our voice will be sampled at 16kHz. The source rate is :
```math
SOURCE RATE = 1 second / 16,000
			= 10^7  / 16,000  * 100ns
            = 625 * 100 ns
```
Hence `SOURCERATE = 625`. 

#### 33. Create Test Paths

Define paths to the testing files in `test.scp`. This is created by executing the following command:

	$ python python_scripts/create_test_scp.py
    
#### 34. Recognize Test Samples
	
`recount.mlf` consists of the predictions of our ASR. This is generated by running our decoder HVite as follows:

	$ Hvite -C config_Hvite  -H hmm15/macros -H hmm15/hmmdefs_kn -S test.scp -i recount.mlf -p 0.0 -s 5.0  -w wdnet -y rec dict-tri tiedlist_kn

Some changes are required in the `recount.mlf` file:
	
- Replace `test_samples` in the path of every `rec` file with an asterisk `*`
- Replace `SENT-START` and `SENT-END` with `sil`

The file should look as shown below:

    "*/ಅದೇ_.rec"
    0 4000000 sil -1541.416870
    4000000 9700000 \340\262\205\340\262\246\340\263\207 -3166.399170
    9700000 15400000 sil -2632.300781
    .
    "*/ಅಧಿಕೃತ_.rec"
    0 3300000 sil -1489.629883
    3300000 12900000 \340\262\205\340\262\247\340\262\277\340\262\225\340\263\203\340\262\244 -5682.479492
    12900000 14500000 sil -737.820129
    .
    "*/ಅಧ್ಯಕ್ಷೀಯ_.rec"
    0 3600000 sil -1499.818726
    3600000 15300000 \340\262\205\340\262\247\340\263\215\340\262\257\340\262\225\340\263\215\340\262\267\340\263\200\340\262\257 -6673.943848
    15300000 23400000 sil -3269.386475
    .

#### 35. Get results

Get the results of analtsis using `HResult` as shown. 

	$ HResults -t -I testref.mlf tiedlist_kn recount.mlf

The option `-t` allows us to additionally see the words that were incorrectly predicted. 


## Small Dictionary Analysis


Instead of the 750 word dictionaries, we also perform analysis for 500 word dictionaries. They are split into 3 separate dictionaries based on word length.

### Triphone-based small dictionary

#### 36. Create Directory tree
In `tri_22K`, go to the `small_syl` directory.

	$ cd small_tri
    
Create the following directories:

    small_syl
        short
             mono
             tri
        middle
             mono
             tri
        long
             mono
             tri
        triphone_resources
        monophone_resuources

Create the triphone dictionaries for short, middle length and long words by executing the following :

	$ python create_small_dict_tri.py
    
 
This creates the following 6 text files:

    small_syl
        short
            tri
                dict_short.txt
                wlist_short.txt
        middle
            tri
                dict_middle.txt
                wlist_middle.txt
        long
            tri
                dict_long.txt
                wlist_long.txt
                
From here, continue onto **Step 38**. Just remember to replace `small_syl` with `small_tri` along the way.

### Syllable-based small dictionary

#### 37. Create Directory Tree for Triphones

In `syl_16K`, go to the `small_syl` directory.

	$ cd small_syl 


Create the following directories:

    small_syl
        short
             mono
             syl
        middle
             mono
             syl
        long
             mono
             syl
        syllable_resources
        monophone_resuources

Copy the `hmm15` directory and `tiedlist_kn` file into the newly created `syllable_resources` directory.

Create the syllable dictionaries by executing the following python file.

	$ python create_small_dict_syl.py

This creates the following 6 text files:

    small_syl
        short
            syl
                dict_short.txt
                wlist_short.txt
        middle
            syl
                dict_middle.txt
                wlist_middle.txt
        long
            syl
                dict_long.txt
                wlist_long.txt


#### 38. Create small Monophone Dictionaries

Similarly create the monophone dictionaries by executing the following.

	$ python create_small_dictionary.py

This creates the following 6 text files:

    small_syl
        short
            mono
                dict_short.txt
                wlist_short.txt
        middle
            mono
                dict_middle.txt
                wlist_middle.txt
        long
            mono
                dict_long.txt
                wlist_long.txt

#### 39. Create small Grammar files

From now onwords, we need every combination of subword (mono, syl) with every dictionary (short, middle, long).

In `create_small_grammar.py`, make sure the folder and subword are initially 'short' and 'mono'. The beginnning of the file should look like the following : 
```
folder = 'short'
subword = 'mono'
```

Now execute the following.

	$ python create_small_grammar.py

This will create the grammar file in the following directory structure:

    small_syl
        short
            mono
                grammar_short


#### 40. Create small test.scp files

In `create_small_test_scp.py` make sure the folder and subword are 'short' and 'mono' respectively as was the case with the previous file. 

We then execute the following command.
	
	$ python create_small_test_scp.py

This creates the following scp file.

    small_syl
        short
            mono
                test_short.scp



#### 41. Create small testref.mlf files
In `create_small_testref_mlf.py` we repeat the same. Make sure folder and subword are 'short' and 'mono' respectively and execute the following command.

	$ python create_small_testref_mlf.py

This creates the `testref` file.

    small_syl
        short
            mono
                testref_short.mlf


_**NOTE** : Changing `short` and `mono` in the code will create the corresponding files._

Repeat the steps , ,and by replacing _short_ with _middle_ and _long_ and replacing _mono_ with _syl_. We should end up with 6 combinations.


#### 42. Fetch Test samples
Copy the `test_samples` from the parent directory to this `small_syl` directory.

Copy `syl_16K/hmm15` and `syl_16K/tiedlist_kn` into `syl_16K/syllable_resources`.

Copy `syl_16K/hmm9` and `syl_16K/monophones1` into `syl_16K/monophone_resources`.

Copy `syl_16K/config_HVite` into `syl_16K/small_syl`.

#### 43. Perform testing

Create grammar file

	$ HParse long/syl/grammar_long long/syl/wdnet_long

Finally execute HVite

	$ Hvite -C config_Hvite  -H syllable_resources/hmm15/macros -H syllable_resources/hmm15/hmmdefs_kn -S long/syl/test_long.scp -i long/syl/recount_long.mlf -p 0.0 -s 5.0  -w long/syl/wdnet_long -y rec long/syl/dict_long.txt syllable_resources/tiedlist_kn

Open `long/syl/recount_long` and :
	
- Replace "test_samples" with "*"
- Replace "SENT-START" and "SENT-END" with "sil"


#### 44. View Results
Now view the results :

	$ HResults -t -I long/syl/testref_long.mlf syllable_resources/tiedlist_kn long/syl/recount_long.mlf

I executed the corresponding code for triphones at 22.05kHz for the small dictionary of "long" words (tri_22K). Here is what I got:



```
Aligned transcription: ಅಕ್ಕಪಕ್ಕದ_.lab vs ಅಕ್ಕಪಕ್ಕದ_.rec
 LAB: sil ಅಕ್ಕಪಕ್ಕದ sil 
 REC: sil ಒಕ್ಕೂಟದ       sil 
Aligned transcription: ಅತ್ಯದ್ಭುತ_.lab vs ಅತ್ಯದ್ಭುತ_.rec
 LAB: sil ಅತ್ಯದ್ಭುತ    sil 
 REC: sil ಕರೆಯಲ್ಪಡುವ sil 
Aligned transcription: ಇಂಡಿಯನ್_.lab vs ಇಂಡಿಯನ್_.rec
 LAB: sil ಇಂಡಿಯನ್ sil 
 REC: sil ಜಿಲ್ಲೆಯ sil 
Aligned transcription: ಉಗಮಗೊಂಡವು_.lab vs ಉಗಮಗೊಂಡವು_.rec
 LAB: sil ಉಗಮಗೊಂಡವು sil 
 REC: sil ಊದುಕೊಳವೆ    sil 
Aligned transcription: ಎಂಭತ್ತು_.lab vs ಎಂಭತ್ತು_.rec
 LAB: sil ಎಂಭತ್ತು sil 
 REC: sil ಒಂಭತ್ತು sil 
Aligned transcription: ಓರೆಗಣ್ಣು_.lab vs ಓರೆಗಣ್ಣು_.rec
 LAB: sil ಓರೆಗಣ್ಣು       sil 
 REC: sil ಹೊಳೆಗಳನ್ನು sil 
Aligned transcription: ಕೊನೆಗೊಂಡ_.lab vs ಕೊನೆಗೊಂಡ_.rec
 LAB: sil ಕೊನೆಗೊಂಡ    sil 
 REC: sil ಕೂಡಿಕೊಂಡು sil 
Aligned transcription: ಖಂಡದದಕ್ಷಿಣ_.lab vs ಖಂಡದದಕ್ಷಿಣ_.rec
 LAB: sil ಖಂಡದದಕ್ಷಿಣ sil 
 REC: sil ಖಂಡನಾಮತ          sil 
Aligned transcription: ಮೊಗ್ಗು_.lab vs ಮೊಗ್ಗು_.rec
 LAB: sil ಮೊಗ್ಗು sil 
 REC: sil ನಾಲ್ಕು sil 
Aligned transcription: ಹದಿನೇಳನೆಯ_.lab vs ಹದಿನೇಳನೆಯ_.rec
 LAB: sil ಹದಿನೇಳನೆಯ sil 
 REC: sil ಹದಿನೇಳನೇ sil 
Aligned transcription: ಹೊಂದಿದ್ದೂ_.lab vs ಹೊಂದಿದ್ದೂ_.rec
 LAB: sil ಹೊಂದಿದ್ದೂ sil 
 REC: sil ಹೊಂದಿದ್ದು sil 
====================== HTK Results Analysis =======================
  Date: Thu Jul  6 14:01:13 2017
  Ref : long/tri/testref_long.mlf
  Rec : long/tri/recount_long.mlf
------------------------ Overall Results --------------------------
SENT: %Correct=97.80 [H=489, S=11, N=500]
WORD: %Corr=99.27, Acc=99.27 [H=1489, D=0, S=11, I=0, N=1500]
===================================================================
```

This is the contents of the file `tri_22K/small_tri/long/tri/incorrect_words.txt`.We get a 97.8% accuracy. The 11 words that were incorrectly predicted are also shown. 

The best performance was achieved by the syllable based ASR at 22.05K for the 500 longest words. I saved the results in `syl_22K/small_syl/long/syl/incorrect_words.txt`. Here are the contents:

```
Aligned transcription: ಅಕ್ಕಪಕ್ಕದ_.lab vs ಅಕ್ಕಪಕ್ಕದ_.rec
 LAB: sil ಅಕ್ಕಪಕ್ಕದ sil 
 REC: sil ಪುಸ್ತಕದ       sil 
Aligned transcription: ಅತ್ಯದ್ಭುತ_.lab vs ಅತ್ಯದ್ಭುತ_.rec
 LAB: sil ಅತ್ಯದ್ಭುತ    sil 
 REC: sil ಕರೆಯಲ್ಪಡುವ sil 
Aligned transcription: ಉರುಗನಹಳ್ಳಿ_.lab vs ಉರುಗನಹಳ್ಳಿ_.rec
 LAB: sil ಉರುಗನಹಳ್ಳಿ sil 
 REC: sil ವರ್ಗದಲ್ಲಿ    sil 
Aligned transcription: ಎಂಭತ್ತು_.lab vs ಎಂಭತ್ತು_.rec
 LAB: sil ಎಂಭತ್ತು sil 
 REC: sil ಒಂಭತ್ತು sil 
Aligned transcription: ಓರೆಗಣ್ಣು_.lab vs ಓರೆಗಣ್ಣು_.rec
 LAB: sil ಓರೆಗಣ್ಣು       sil 
 REC: sil ಹೊಳೆಗಳನ್ನು sil 
Aligned transcription: ಕೊನೆಗೊಂಡ_.lab vs ಕೊನೆಗೊಂಡ_.rec
 LAB: sil ಕೊನೆಗೊಂಡ    sil 
 REC: sil ಕೂಡಿಕೊಂಡು sil 
Aligned transcription: ಖಂಡದದಕ್ಷಿಣ_.lab vs ಖಂಡದದಕ್ಷಿಣ_.rec
 LAB: sil ಖಂಡದದಕ್ಷಿಣ sil 
 REC: sil ಖಂಡನಾಮತ          sil 
Aligned transcription: ಮೊಗ್ಗು_.lab vs ಮೊಗ್ಗು_.rec
 LAB: sil ಮೊಗ್ಗು sil 
 REC: sil ನಾಲ್ಕು sil 
Aligned transcription: ಹದಿನೇಳನೆಯ_.lab vs ಹದಿನೇಳನೆಯ_.rec
 LAB: sil ಹದಿನೇಳನೆಯ sil 
 REC: sil ಹದಿನೇಳನೇ sil 
====================== HTK Results Analysis =======================
  Date: Fri Jun  2 16:37:44 2017
  Ref : long/syl/testref_long.mlf
  Rec : long/syl/recount_long.mlf
------------------------ Overall Results --------------------------
SENT: %Correct=98.20 [H=491, S=9, N=500]
WORD: %Corr=99.40, Acc=99.40 [H=1491, D=0, S=9, I=0, N=1500]
===================================================================
```


Perform Testing and evaluation using steps 29 to 35 using the corresponding small dictionary, grammar and mlf files. Furthermore, remember to  use `syllable_resources/tiedlist_kn` for the tiedlist and `syllable_resources/hmmdefs_kn`for hmmdefs. In the case of monophone based ASR, use the corresponding files in `monophone_resources`

You should be good to go! 


