
from RP import RP

rp = RP()
rp.set_file_name("example.pdf")
rp.get_text()
rp.get_stop_words()
#rp.display_sws()
rp.get_words()
rp.set_n_limit(8)
rp.get_n_grams()
rp.filter_n_grams()
rp.get_n_gram_counts()
rp.sort_n_grams()
#rp.display_n_gram_counts()
rp.display_n_grams()


