# LdG simulation development journal

#### Todo list
- 2D slice
- load data
- C-Python API

#### `utility.py`
> 模組間共用函數

2020/02/15 新增`show()`、`Q_tensor()`  
2020/02/17 新增`cartesian()`、`distance()`  
2020/02/21 修改`cartesian()`，增加使用彈性  
2020/02/22 改寫`show()`為grid-based版本，`distance()`用`norm()`取代，改寫`Q_tensor()`加入修正項，比較"pure python"和"using numpy"的執行效率(前者較優，迭代10萬次，後者用時約為前者2倍)

#### `param.py`
> 物理參數設定

2020/02/10 完成參數部分的設定  
2020/02/15 完成網格設定  
2020/02/19 網格物件化  
2020/02/20 把網格定義、網格生成拆分成另外的檔案  
2020/03/23 新增邊界條件和初始條件的參數  

#### `mesh.py`
> 網格定義、網格生成

2020/02/20 網格定義、網格生成  
2020/02/22 強制`r`為`ndarray`，讓`n`可接受2D或3D的array-like物件且強制normalize  
2020/02/24 新增`_h`、`_Q`屬性，含getter、setter
2020/03/21 改成absolute import  

#### `cond.py`
> 邊界條件和初始條件

2020/02/17 完成 surface anchoring 部分，剩下 substrate 部分  
2020/02/19 發現`envelope()`定義有問題  
2020/02/21 新增`rotate()`，並進行surface anchoring初步視覺化，架構待整理  
2020/02/17 完成主功能(element-wise)，寫檔和vectorize還沒  
2020/02/24 修正「一旋轉圖就不見」的問題(`retrive()`的回傳類型不一致)、新增`reorder()`設定S的邊界條件  
2020/02/22 合併`bcond.py`和`icond.py`，重構  
2020/03/21 改成absolute import  

#### `solver.py`
> 尤拉方程數值解

2020/02/17 pseudocode  
2020/02/22 重新命名，並將Q、n/S間的轉換納入規劃  
2020/02/24 新增`retrive_Q()`、`laplace()`、`h()`、`state_evolve()`，未完  
2020/03/21 改成absolute import，新增`gradient()`、`eigen()`、修改`laplace()`  
2020/05/06 解決迭代過程中traceless和asymmetric的問題  

#### `output.py`
> 輸出數據視覺化

2020/02/20 畫圖測試邊界條件，但有問題  
2020/02/22 封裝成`streamline()`並畫出r field做測試，新增`retrive_r()`、`retrive_n()`並vectorize  
2020/02/24 新增`sphere`、`hedgehog`  
2020/03/21 改成absolute import  
2020/03/23 新增存檔功能`save()`  

#### `main.py`
> 主程式

2020/02/22 發現bug，n場經過`rotate()`之後會消失，目前還沒找到原因  
2020/03/21 改成absolute import  
2020/03/23 加入iteration步驟  

#### `image/`
> 圖庫

2020/02/21 新增 `surface_anchoring.png`：顯示球表面液晶分子走向  
2020/02/23 新增 `BC_surface_anchoring.png`：修正球表面液晶分子走向  