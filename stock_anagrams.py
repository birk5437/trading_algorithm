import re, urllib, sqlite3, string
from time import gmtime, strftime
 
def get_quote(symbol):
  base_url = 'http://finance.google.com/finance?q='
  content = urllib.urlopen(base_url + symbol).read()
  find_q = re.search(r'\<span\sid="ref_\d+.*">(.+)<', content)
  if find_q:
    quote = find_q.group(1)
  else:
    quote = 0
        #'no quote available for: %s' % symbol
  return quote
 
def main():
  #print get_quote('ibm') #168.28
  connection = sqlite3.connect('stocks.db')
  cursor = connection.cursor()
    
  #Test of 5 companys
  #Companys = ['DJIA', 'GOOG', 'BURKE', 'MSFT', 'AAPL', 'NVDA', 'TTM']
  #for i,value in enumerate(Companys):
  for letter1 in string.ascii_uppercase.lstrip('AB'):
    symbol = letter1
    v_quote = string.replace(str(get_quote(symbol)),',','')
    if v_quote != "0":
      print '%s --> %s' %  (symbol,v_quote)
      date = strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
      sql = "insert into quote (QUOTE_SYMBOL, QUOTE_PRICE, QUOTE_DT) values(\'" + symbol + "\'," + v_quote + ",\'" + date + "\')"
      cursor.execute(sql)
      connection.commit()    
    for letter2 in string.ascii_uppercase:
      symbol = letter1 + letter2
      v_quote = string.replace(str(get_quote(symbol)),',','')
      if v_quote != "0":
        print '%s --> %s' %  (symbol,v_quote)
        date = strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
        sql = "insert into quote (QUOTE_SYMBOL, QUOTE_PRICE, QUOTE_DT) values(\'" + symbol + "\'," + v_quote + ",\'" + date + "\')"
        cursor.execute(sql)
        connection.commit()
      for letter3 in string.ascii_uppercase:
        symbol = letter1 + letter2 + letter3
        v_quote = string.replace(str(get_quote(symbol)),',','')
        if v_quote != "0":
          print '%s --> %s' %  (symbol,v_quote)
          date = strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
          sql = "insert into quote (QUOTE_SYMBOL, QUOTE_PRICE, QUOTE_DT) values(\'" + symbol + "\'," + v_quote + ",\'" + date + "\')"
          #print sql
          cursor.execute(sql)
          connection.commit()
        '''Output-->
        google --> 525.10
        ibm --> 168.28
        microsoft --> 25.52
        apple --> 350.70
        nvidia --> 18.52
        '''
  connection.close()
 
if __name__ == "__main__":
  main()
