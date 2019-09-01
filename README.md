# py-apis.my
Py 寫的小工具，底層是FLASK。
目前有：
1. Meta Proxy


### 1. Meta Proxy，輸入網址可以取得特定的meta資訊，for 特定用途

使用情況，懶得去DB撈文章的資料

- [x] 依據天下集團的文章ID取得文章網頁的meta，用type區分頻道
- [x] 依據網址取得網頁的meta
- [x] 輸出成json
- [x] default cache for 1h, cache to build, nocache to revoke
- [x] 網址換成短網址
- [x] 可以自行定義utm參數

#### Entrypoint: [GET] /metaproxy

#### Parameters

|Parameters|Description|
|----------|-----------|
|`id`|文章ID|
|`type`|文章分類：cw, futurecity, opinion, ch, cheers|
|`url`|也可以直接指定文章的url，順序以id為優先|
|`utm_campaign`|不解釋|
|`utm_medium`|不解釋|
|`utm_source`|不解釋|
|`cache`|`1`: 強制重新建立快取|
|`nocache`|`1`: 不使用快取|


