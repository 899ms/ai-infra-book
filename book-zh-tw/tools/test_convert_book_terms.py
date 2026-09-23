from convert_book import convert_text


def test_technical_terms_preserve_meaning():
    assert convert_text('算子库') == '運算子庫'
    assert convert_text('矩阵算子') == '矩陣運算子'
    assert convert_text('运算子') == '運算子'
    assert convert_text('運算子') == '運算子'
    assert convert_text('演算子') == '演算子'
    assert convert_text('运算元') == '運算元'
    assert convert_text('卸载权重') == '卸載權重'
    assert convert_text('程序代码') == '程式碼'
    assert convert_text('进程编号') == '行程編號'
    assert convert_text('工具程序可以通过操作系统访问文件') == '工具程式可以透過作業系統存取檔案'
    assert convert_text('工具程序仍由操作系统执行') == '工具行程仍由作業系統執行'
    assert convert_text('CPU\n提交程序') == 'CPU\n提交行程'
    assert convert_text('激活参数量') == '每 token 選用參數量'
    assert convert_text('每 token 激活约 37B') == '每 token 選用約 37B'
    assert convert_text('激活规模') == '每 token 選用參數規模'
    assert convert_text('MoE 激活量') == 'MoE 每 token 選用參數量'
    assert convert_text('每个 token 实际激活的参数') == '每個 token 實際選用的參數'
    assert convert_text('一个 token 激活多少参数') == '一個 token 選用多少參數'
    assert convert_text('稀疏激活') == '稀疏路由'
    assert convert_text('被激活路径') == '被選用路徑'
    assert convert_text('激活 FLOPs') == '選用路徑的 FLOPs'
    assert convert_text('行激活') == '行啟用'
    assert convert_text('激活') == '活化'
    assert convert_text('激活函数') == '活化函數'
    assert convert_text('激活张量') == '活化張量'
    assert convert_text('激活值') == '活化值'
    assert convert_text('中间向量称为激活') == '中間向量稱為活化值'
    assert convert_text('激活的生命周期') == '活化值的生命週期'
    assert convert_text('未通过测试的补丁') == '未通過測試的補丁'
    assert convert_text('通過測試') == '通過測試'
    assert convert_text('通过 PCIe 外设') == '透過 PCIe 外設'
    assert convert_text('水平线') == '水平線'
    assert convert_text('水平點線') == '水平點線'
    assert convert_text('曲线接近水平') == '曲線接近水平'
    assert convert_text('达到什么水平') == '達到什麼水準'
    assert convert_text('实现的行为') == '實現的行為'
    assert convert_text('实现原子性、一致性、隔离性和持久性') == '實現原子性、一致性、隔離性與持久性'


if __name__ == '__main__':
    test_technical_terms_preserve_meaning()
    print('technical terminology conversion checks passed')
