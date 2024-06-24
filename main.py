import streamlit as st
import sqlite3
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def create_users_table():
    conn = sqlite3.connect('users.db', check_same_thread=False)
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS users(username TEXT, password TEXT)')
    conn.commit()
    conn.close()

def add_user(username, password):
    conn = sqlite3.connect('users.db', check_same_thread=False)
    c = conn.cursor()
    hashed_password = hash_password(password)
    c.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_password))
    conn.commit()
    conn.close()

def delete_user(username):
    conn = sqlite3.connect('users.db', check_same_thread=False)
    c = conn.cursor()
    c.execute('DELETE FROM users WHERE username = ?', (username,))
    conn.commit()
    conn.close()

def check_user(username, password):
    conn = sqlite3.connect('users.db', check_same_thread=False)
    c = conn.cursor()
    hashed_password = hash_password(password)
    c.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, hashed_password))
    data = c.fetchall()
    conn.close()
    return len(data) != 0

def main_app():
    st.title('取締役会・経営会議議案タイトル検索')

    option1 = st.selectbox(
        '法人名（日本法人の場合空白を選択）',
        ['', '台湾法人', '香港法人', 'US法人']
    )

    option3 = st.selectbox(
        'ブランド名（ブランド名がないか、関係ない場合空白を選択）',
        ['BAKE CHEESE TART', 'RINGO', 'ZAKUZAKU', 'PRESS BUTTER SAND', '八 by PRESS BUTTER SAND', 'caica', 'しろいし洋菓子店', 'オンラインチャネル', 'cake.tokyo', '新ブランド', '']
    )

    option4 = st.selectbox(
        '内容（ない場合空白を選択し、下記に検索ワードを記入）',
        ['出店', '卸', '期間限定販売', '販売', '']
    )

    text_input5 = st.text_input('フリーワード検索（複数不可）')

    if st.button('検索スタート'):
        dbname = 'GIAN_TITLE.db'
        conn = sqlite3.connect(dbname, check_same_thread=False)
        cur = conn.cursor()

        st.subheader('基本形')

        sql_query = "SELECT date, meeting, title FROM titles WHERE date = '基本形' AND title LIKE ? AND title LIKE ? AND title LIKE ?"
        params = ('%' + option3 + '%', '%' + option4 + '%', '%' + text_input5 + '%')
        cur.execute(sql_query, params)
        for row in cur:
            st.dataframe(row, use_container_width=True)

        st.subheader('実際のタイトル例')

        sql_query = "SELECT date, meeting, title FROM titles WHERE NOT (date='基本形') AND title LIKE ? AND title LIKE ? AND title LIKE ? AND title LIKE ?"
        params = ('%' + option1 + '%', '%' + option3 + '%', '%' + option4 + '%', '%' + text_input5 + '%')
        cur.execute(sql_query, params)

        for row in cur:
            st.dataframe(row, use_container_width=True)


# 管理者用のデータベース操作関数を追加
def admin_add_title(date, meeting, title):
    conn = sqlite3.connect('GIAN_TITEL.db', check_same_thread=False)
    c = conn.cursor()
    c.execute('INSERT INTO titles (date, meeting, title) VALUES (?, ?, ?)', (date, meeting, title))
    conn.commit()
    conn.close()

def admin_delete_title(title_id):
    conn = sqlite3.connect('GIAN_TITEL.db', check_same_thread=False)
    c = conn.cursor()
    c.execute('DELETE FROM titles WHERE rowid = ?', (title_id,))
    conn.commit()
    conn.close()

def admin_dashboard():
    st.subheader("管理者ダッシュボード")

    with st.expander("ユーザー管理"):
        new_user = st.text_input("新規ユーザー名", key="new_user")
        new_password = st.text_input("新規パスワード", type='password', key="new_password")
        if st.button("ユーザー追加"):
            add_user(new_user, new_password)
            st.success("ユーザーを追加しました。")

        del_user = st.text_input("削除ユーザー名", key="del_user")
        if st.button("ユーザー削除"):
            delete_user(del_user)
            st.success("ユーザーを削除しました。")

    with st.expander("議案の追加と削除"):
        date = st.text_input("日付")
        meeting = st.text_input("会議名")
        title = st.text_input("議案名")
        if st.button("議案を追加"):
            admin_add_title(date, meeting, title)
            st.success("議案が追加されました。")

        title_id = st.text_input("削除する議案のID")
        if st.button("議案を削除"):
            admin_delete_title(title_id)
            st.success("議案が削除されました。")

def main():
    st.sidebar.title("本人認証")
    menu = ["Home", "Login", "SignUp"]
    choice = st.sidebar.radio("Menu", menu)

    if choice == "Home":
        st.subheader("Home")

    elif choice == "Login":
        username = st.sidebar.text_input("User Name")
        password = st.sidebar.text_input("Password", type='password')
        if st.sidebar.button("Login"):
            if check_user(username, password):
                st.session_state['logged_in'] = True
                st.session_state['username'] = username
                st.success("Login successful")
                if username == 'admin':
                    st.session_state['admin'] = True
            else:
                st.warning("Incorrect Username/Password")

    elif choice == "SignUp":
        new_user = st.text_input("Username")
        new_password = st.text_input("Password", type='password')
        if st.button("Signup"):
            add_user(new_user, new_password)
            st.success("You have successfully created an account.")
            st.info("Go to Login Menu to login")

    if 'logged_in' in st.session_state and st.session_state['logged_in']:
        if 'admin' in st.session_state and st.session_state['admin']:
            admin_dashboard()  # 管理者のみがアクセス可能なダッシュボード
        else:
            main_app()  # 通常のユーザー用ダッシュボード

if __name__ == "__main__":
    create_users_table()
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
    main()
