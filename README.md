
## Requirements

```
tensorflow==1.8.0
tensorflow-serving-api==1.8.0==1.8.0
```

## Example

### export sample model

```bash
rm -rf models
python example_model.py
```

### create warmup data

```bash
python warmup.py --export_dir models/0 --name demo
```

### dock run tfserving image

```bash
docker run -p 8500:8500 -it --mount type=bind,source=`pwd`,destination=/work tensorflow/serving:1.8.0-devel /bin/bash
```

### start serving process in docker image

```bash
cd /work
tensorflow_model_server --model_config_file=model.config --platform_config_file=platform.config
```

```log
root@1d26b7f44fc4:/work# tensorflow_model_server --model_config_file=model.config --platform_config_file=platform.config
2019-03-14 02:55:12.702456: I tensorflow_serving/model_servers/server_core.cc:444] Adding/updating models.
2019-03-14 02:55:12.702541: I tensorflow_serving/model_servers/server_core.cc:499]  (Re-)adding model: demo
2019-03-14 02:55:12.833040: I tensorflow_serving/core/basic_manager.cc:716] Successfully reserved resources to load servable {name: demo version: 0}
2019-03-14 02:55:12.833109: I tensorflow_serving/core/loader_harness.cc:66] Approving load for servable version {name: demo version: 0}
2019-03-14 02:55:12.833142: I tensorflow_serving/core/loader_harness.cc:74] Loading servable version {name: demo version: 0}
2019-03-14 02:55:12.834499: I external/org_tensorflow/tensorflow/contrib/session_bundle/bundle_shim.cc:360] Attempting to load native SavedModelBundle in bundle-shim from: /work/models/0
2019-03-14 02:55:12.835285: I external/org_tensorflow/tensorflow/cc/saved_model/loader.cc:242] Loading SavedModel with tags: { serve }; from: /work/models/0
2019-03-14 02:55:12.842170: I external/org_tensorflow/tensorflow/core/platform/cpu_feature_guard.cc:140] Your CPU supports instructions that this TensorFlow binary was not compiled to use: AVX2 FMA
2019-03-14 02:55:12.855920: I external/org_tensorflow/tensorflow/cc/saved_model/loader.cc:161] Restoring SavedModel bundle.
2019-03-14 02:55:12.858568: I external/org_tensorflow/tensorflow/cc/saved_model/loader.cc:171] The specified SavedModel has no variables; no checkpoints were restored.
2019-03-14 02:55:12.858717: I external/org_tensorflow/tensorflow/cc/saved_model/loader.cc:196] Running LegacyInitOp on SavedModel bundle.
2019-03-14 02:55:12.859584: I external/org_tensorflow/tensorflow/cc/saved_model/loader.cc:291] SavedModel load for tags { serve }; Status: success. Took 24338 microseconds.
2019-03-14 02:55:12.915672: I tensorflow_serving/servables/tensorflow/saved_model_warmup.cc:121] Finished reading warmup data for model at /work/models/0/assets.extra/tf_serving_warmup_requests. Number of warmup records read: 256.
2019-03-14 02:55:12.932273: I tensorflow_serving/core/loader_harness.cc:86] Successfully loaded servable version {name: demo version: 0}
2019-03-14 02:55:12.934373: I tensorflow_serving/model_servers/main.cc:323] Running ModelServer at 0.0.0.0:8500 ...
```

