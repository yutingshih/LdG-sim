# LdG simulation development journal

#### `utility.py`
> 模組間共用函數

2020/02/15 新增show()、Q_tensor()  
2020/02/17 新增cartesian()、distance()  
2020/02/21 修改cartesian()，增加使用彈性  

#### `param.py`
> 物理參數設定

2020/02/10 完成參數部分的設定  
2020/02/15 完成網格設定  
2020/02/19 網格物件化  
2020/02/20 把網格定義、網格生成拆分成另外的檔案

#### `mesh.py`
> 網格定義、網格生成

2020/02/20 網格定義、網格生成

#### `bcond.py`
> 邊界條件

2020/02/17 完成 surface anchoring 部分，剩下 substrate 部分  
2020/02/19 發現envelope定義有問題
2020/02/21 新增rotate()，並進行surface anchoring初步視覺化，架構待整理

#### `icond.py`
> 初始條件

2020/02/17 完成主功能(element-wise)，寫檔和 vectorize 還沒  

#### `iterate.py`
> 尤拉方程數值解

2020/02/17 pseudocode  

#### `output.py`
> 輸出數據視覺化

2020/02/20 畫圖測試邊界條件，但有問題

#### `image/`
> 圖庫

2020/02/21 新增 `surface_anchoring.png`：顯示球表面液晶分子走向