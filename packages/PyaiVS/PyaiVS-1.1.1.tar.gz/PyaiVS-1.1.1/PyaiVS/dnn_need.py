from PyaiVS import model_bulid
model_bulid.running('/data/jianping/bokey/OCAICM/dataset/aurorab/aurorab.csv',out_dir='/data/jianping/bokey/OCAICM/dataset/',
                    split='all',model=['SVM','KNN','DNN','RF','XGB'],FP='all', run_type='result',cpus=6)