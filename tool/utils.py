import re
import math 


s1 = u'ÀÁÂÃÈÉÊÌÍÒÓÔÕÙÚÝàáâãèéêìíòóôõùúýĂăĐđĨĩŨũƠơƯưẠạẢảẤấẦầẨẩẪẫẬậẮắẰằẲẳẴẵẶặẸẹẺẻẼẽẾếỀềỂểỄễỆệỈỉỊịỌọỎỏỐốỒồỔổỖỗỘộỚớỜờỞởỠỡỢợỤụỦủỨứỪừỬửỮữỰựỲỳỴỵỶỷỸỹ'
s0 = u'AAAAEEEIIOOOOUUYaaaaeeeiioooouuyAaDdIiUuOoUuAaAaAaAaAaAaAaAaAaAaAaAaEeEeEeEeEeEeEeEeIiIiOoOoOoOoOoOoOoOoOoOoOoOoUuUuUuUuUuUuUuYyYyYyYy'

def get_individual_from_title(input_str):
	try:
		if math.isnan(input_str):
			return "nan"
	except:
		k = 1
	s = ''
	for c in input_str:
		if c in s1:
			s += s0[s1.index(c)]
		else:
			s += c
	s = remove_special_chars_keep_punct_space(s)
	s = re.sub(r'\s', '', s)
	return s.replace(" ", "").lower().replace("|", "")


def remove_special_chars_keep_punct_space(text):
	if text == "nan":
		return "nan"
	if type(text) is not str and  math.isnan(text):
		return "nan"
	else:
		# print(text)
		return re.sub(r"[^\w\s]", "", text)

# print(get_individual_from_title("Рецепт хорошего сна 7 дней до ощущения бодрости после сна"))
