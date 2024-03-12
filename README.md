# Инжиниринг данных. Домашнее задание 1 (HW)

Установка зависимостей:
```bash
poetry install
```

Запуск пайплайна:
```bash
poetry run python -m src.main
```

<details><summary>
Логи успешного выполнения:
</summary>
```log
DEBUG: Checking if NCBIArchiveLoaderTask() is complete
DEBUG: Checking if NCBIEndpointDatasetGetterTask(dataset_name=GSE68849) is complete
INFO: Informed scheduler that task   NCBIArchiveLoaderTask__99914b932b   has status   PENDING
INFO: Informed scheduler that task   NCBIEndpointDatasetGetterTask_GSE68849_e34547c091   has status   PENDING
DEBUG: Checking if NCBIEndpointDatasetGetterTask(dataset_name=GSE68849) is complete
INFO: Informed scheduler that task   NCBIEndpointDatasetGetterTask_GSE68849_e34547c091   has status   PENDING
DEBUG: Checking if NCBIExtractTarFileTask() is complete
DEBUG: Checking if NCBIArchiveLoaderTask() is complete
INFO: Informed scheduler that task   NCBIExtractTarFileTask__99914b932b   has status   PENDING
DEBUG: Checking if NCBIEndpointDatasetGetterTask(dataset_name=GSE68849) is complete
INFO: Informed scheduler that task   NCBIArchiveLoaderTask__99914b932b   has status   PENDING
INFO: Informed scheduler that task   NCBIEndpointDatasetGetterTask_GSE68849_e34547c091   has status   PENDING
DEBUG: Checking if NCBIDataSetsProcessingTask() is complete
/Users/sber-market/PycharmProjects/personal/mfti/second-semester/de-hw-1/.venv/lib/python3.11/site-packages/luigi/worker.py:426: UserWarning: Task NCBIDataSetsProcessingTask() without outputs has no custom complete() method
  is_complete = task.complete()
DEBUG: Checking if NCBIExtractTarFileTask() is complete
INFO: Informed scheduler that task   NCBIDataSetsProcessingTask__99914b932b   has status   PENDING
DEBUG: Checking if NCBIArchiveLoaderTask() is complete
INFO: Informed scheduler that task   NCBIExtractTarFileTask__99914b932b   has status   PENDING
DEBUG: Checking if NCBIEndpointDatasetGetterTask(dataset_name=GSE68849) is complete
INFO: Informed scheduler that task   NCBIArchiveLoaderTask__99914b932b   has status   PENDING
INFO: Informed scheduler that task   NCBIEndpointDatasetGetterTask_GSE68849_e34547c091   has status   PENDING
INFO: Done scheduling tasks
INFO: Running Worker with 1 processes
DEBUG: Asking scheduler for work...
DEBUG: Pending tasks: 4
INFO: [pid 10804] Worker Worker(salt=3563868436, workers=1, host=Mac-Studio-madara.local, username=sber-market, pid=10804) running   NCBIEndpointDatasetGetterTask(dataset_name=GSE68849)
2024-03-13 02:16:20.577 | INFO     | src.pipelines:run:27 - Running EndpointDatasetGetterTask...
2024-03-13 02:16:21.528 | SUCCESS  | src.pipelines:run:30 - Got NCBI page!
2024-03-13 02:16:21.528 | SUCCESS  | src.pipelines:run:34 - Saved download endpoint https://www.ncbi.nlm.nih.gov/geo/download/?acc=GSE68849&format=file to data/output/GSE68849_url.txt
INFO: [pid 10804] Worker Worker(salt=3563868436, workers=1, host=Mac-Studio-madara.local, username=sber-market, pid=10804) done      NCBIEndpointDatasetGetterTask(dataset_name=GSE68849)
DEBUG: 1 running tasks, waiting for next task to finish
INFO: Informed scheduler that task   NCBIEndpointDatasetGetterTask_GSE68849_e34547c091   has status   DONE
DEBUG: Asking scheduler for work...
DEBUG: Pending tasks: 3
INFO: [pid 10804] Worker Worker(salt=3563868436, workers=1, host=Mac-Studio-madara.local, username=sber-market, pid=10804) running   NCBIArchiveLoaderTask()
2024-03-13 02:16:21.530 | INFO     | src.pipelines:run:80 - Running NCBIArchiveLoader...
2024-03-13 02:16:21.530 | INFO     | src.pipelines:run:85 - Downloading archive from https://www.ncbi.nlm.nih.gov/geo/download/?acc=GSE68849&format=file...
2024-03-13 02:16:36.309 | SUCCESS  | src.pipelines:run:88 - Downloaded archive from https://www.ncbi.nlm.nih.gov/geo/download/?acc=GSE68849&format=file!
2024-03-13 02:16:36.317 | SUCCESS  | src.pipelines:run:92 - Saved archive to data/output/NCBI_GEO_Dataset_RAW.tar
INFO: [pid 10804] Worker Worker(salt=3563868436, workers=1, host=Mac-Studio-madara.local, username=sber-market, pid=10804) done      NCBIArchiveLoaderTask()
DEBUG: 1 running tasks, waiting for next task to finish
INFO: Informed scheduler that task   NCBIArchiveLoaderTask__99914b932b   has status   DONE
DEBUG: Asking scheduler for work...
DEBUG: Pending tasks: 2
INFO: [pid 10804] Worker Worker(salt=3563868436, workers=1, host=Mac-Studio-madara.local, username=sber-market, pid=10804) running   NCBIExtractTarFileTask()
2024-03-13 02:16:36.344 | SUCCESS  | src.pipelines:run:119 - Extracted archive data/output/NCBI_GEO_Dataset_RAW.tar to data/output!
2024-03-13 02:16:36.685 | SUCCESS  | src.pipelines:run:131 - Saved extracted files to data/output/extracted_files.txt
INFO: [pid 10804] Worker Worker(salt=3563868436, workers=1, host=Mac-Studio-madara.local, username=sber-market, pid=10804) done      NCBIExtractTarFileTask()
DEBUG: 1 running tasks, waiting for next task to finish
INFO: Informed scheduler that task   NCBIExtractTarFileTask__99914b932b   has status   DONE
DEBUG: Asking scheduler for work...
DEBUG: Pending tasks: 1
INFO: [pid 10804] Worker Worker(salt=3563868436, workers=1, host=Mac-Studio-madara.local, username=sber-market, pid=10804) running   NCBIDataSetsProcessingTask()
2024-03-13 02:16:38.076 | SUCCESS  | src.pipelines:_save_processed_datasets:244 - Saved processed dataset to data/tsv/Heading_FULL_2024-03-12_23:16:38.075432+00:00.tsv
2024-03-13 02:16:39.670 | SUCCESS  | src.pipelines:_save_processed_datasets:244 - Saved processed dataset to data/tsv/Probes_FULL_2024-03-12_23:16:38.076687+00:00.tsv
2024-03-13 02:16:39.673 | SUCCESS  | src.pipelines:_save_processed_datasets:244 - Saved processed dataset to data/tsv/Controls_FULL_2024-03-12_23:16:39.670143+00:00.tsv
2024-03-13 02:16:39.673 | SUCCESS  | src.pipelines:_save_processed_datasets:244 - Saved processed dataset to data/tsv/Columns_FULL_2024-03-12_23:16:39.673255+00:00.tsv
2024-03-13 02:16:40.069 | SUCCESS  | src.pipelines:_save_processed_datasets:244 - Saved processed dataset to data/tsv/Probes_PARTIAL_2024-03-12_23:16:39.689820+00:00.tsv
2024-03-13 02:16:40.070 | SUCCESS  | src.pipelines:_drop_unnecessary_files:274 - Removed data/GPL10558_HumanHT-12_V4_0_R1_15002873_B.txt
2024-03-13 02:16:40.072 | SUCCESS  | src.pipelines:_drop_unnecessary_files:274 - Removed data/GPL10558_HumanHT-12_V4_0_R2_15002873_B.txt
INFO: [pid 10804] Worker Worker(salt=3563868436, workers=1, host=Mac-Studio-madara.local, username=sber-market, pid=10804) done      NCBIDataSetsProcessingTask()
DEBUG: 1 running tasks, waiting for next task to finish
INFO: Informed scheduler that task   NCBIDataSetsProcessingTask__99914b932b   has status   DONE
DEBUG: Asking scheduler for work...
DEBUG: Done
DEBUG: There are no more tasks to run at this time
INFO: Worker Worker(salt=3563868436, workers=1, host=Mac-Studio-madara.local, username=sber-market, pid=10804) was stopped. Shutting down Keep-Alive thread
INFO: 
===== Luigi Execution Summary =====

Scheduled 4 tasks of which:
* 4 ran successfully:
    - 1 NCBIArchiveLoaderTask()
    - 1 NCBIDataSetsProcessingTask()
    - 1 NCBIEndpointDatasetGetterTask(dataset_name=GSE68849)
    - 1 NCBIExtractTarFileTask()

This progress looks :) because there were no failed tasks or missing dependencies

===== Luigi Execution Summary =====
```
</details>


<details><summary>
Результат работы:
</summary>
![work_result_info.png](work_result_info.png)
</details>
