import matplotlib.pyplot as plt
import csv
import pandas as pd

x = []
y = []


dataframe = pd.read_csv('CHCL.csv', index_col = 0, parse_dates = True)
dataframe1 = pd.read_csv('CHCL1.csv',index_col = 0, parse_dates = True)


f, (ax1, ax2) = plt.subplots(2, sharex=True, sharey=True)
plt.xlabel('Date')
ax1.set_ylabel('Closing Price(uncleaned dataset')

ax1.plot(dataframe['Closing Price'])

ax1.set_title('Chilime Hydropower Company Limited')

# ax2.plot(dataframe['Minimum Price'])
# ax2.set_ylabel('Minimum Price')



ax2.plot(dataframe1['Closing Price'])
ax2.set_ylabel('Closing Price(Cleaned dataset)')


# # Fine-tune figure; make subplots close to each other and hide x ticks for
# # all but bottom plot.
f.subplots_adjust(hspace=0)
plt.setp([a.get_xticklabels() for a in f.axes[:-1]], visible=False)
plt.show()

# plt.figure()



# ax1 = plt.subplot2grid((6,1), (0,0), rowspan=1, colspan=1)
# ax1.set_title('Sharing both axes')

# ax2 = plt.subplot2grid((6,1), (1,0), rowspan=4, colspan=1)
# ax1.set_title('Sharing both axes')
# ax3 = plt.subplot2grid((6,1), (5,0), rowspan=1, colspan=1)
# ax2.set_title('Sharing both axes')






# plt.xlabel('Date')
# plt.ylabel('Price')


# #plt.legend()
# plt.subplots_adjust(left=0.11, bottom=0.24, right=0.90, top=0.90, wspace=0.2, hspace=0)
# plt.show()
