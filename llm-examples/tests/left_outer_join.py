import pandas as pd

def left_outer_join(df_left, df_right, on='id') -> pd.DataFrame:
    # https://stackoverflow.com/questions/50543326/how-to-do-left-outer-join-exclusion-in-pandas
    # indicator=True parameter adds a column to the output dataframe called _merge that indicates the source of each row.
    df = pd.merge(df_left, df_right, on=[on], how="left", indicator=True
              ).query('_merge=="left_only"')
    # delete the _merge column
    df = df.drop(columns=['_merge'])
    return df
    

def exp1():
    df_left = pd.DataFrame({'id': ['a', 'b', 'c', 'd']})
    df_right = pd.DataFrame({'id': ['b', 'e']})

    left_joined = left_outer_join(df_left, df_right)
    print(left_joined)


def exp2():
    df_left = pd.DataFrame({'id': ['a']})
    df_right = pd.DataFrame({'id': ['b', 'e']})

    left_joined = left_outer_join(df_left, df_right)
    print(left_joined)



if __name__ == '__main__':
    exp1()
    exp2()


