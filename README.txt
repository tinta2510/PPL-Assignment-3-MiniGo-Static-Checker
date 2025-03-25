Change current directory to initial/src where there is file run.py
Type: python run.py gen 
Then type: python run.py test CheckerSuite

reduce(
 # NẾU LÀ Symbol mới được đưa vào bảng Symbol và cập nhật phần tử trả về tại trí đầu của bảng Symbol
  lambda acc, ele: [
      ([result] + acc[0]) if isinstance(result := self.visit(ele, acc), Symbol) else acc[0]
  ] + acc[1:], 
  # LỌC RA method/function/var
  filter(lambda item: isinstance(item, Decl), ast.decl), 
 # TẦM VỰC ĐẦU TIÊN SẼ LÀ DANH SÁCH CÁC HÀM
  [[
      Symbol("getInt", FuntionType()),
      Symbol("putInt", FuntionType()),
      Symbol("putIntLn", FuntionType()),
      # TODO: Implement
  ]]
) 