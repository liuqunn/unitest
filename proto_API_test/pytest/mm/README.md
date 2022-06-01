# 命令等价
python -m pytest | pytest

# 指定函数名执行
pytest -k test_abc -s

# 指定mark执行
pytest -m test01 -s

# 重复执行次数
pytest -s --count 5