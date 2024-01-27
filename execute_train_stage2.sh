
#cp ${exp_dir}/best-valid-loss.pt ${exp_dir}/epoch-2.pt  # --start-epoch 3=2+1

CUDA_VISIBLE_DEVICES=6 python3 train.py \
	--filter-min-duration 0.5 \
	--filter-max-duration 14 \
	--train-stage 2 \
	--dtype "float32" \
	--save-every-n 10000 \
	--valid-interval 20000 \
	--model-name valle \
	--share-embedding true \
	--norm-first true \
	--add-prenet false \
	--decoder-dim 1024 \
	--nhead 16 \
	--num-decoder-layers 12 \
	--prefix-mode 1 \
	--base-lr 0.05 \
	--warmup-steps 200 \
	--average-period 0 \
	--num-epochs 100 \
	--start-epoch 159 \
	--start-batch 0 \
	--accumulate-grad-steps 4 \
	--train_dir dataset/train \
	--valid_dir dataset/test \
	--exp-dir exp/vall-e-x
