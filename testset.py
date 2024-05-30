import streamlit as st
import mysql.connector
from datetime import date

# Define the connection parameters
username = 'ywl'
password = 'ebi8177767!'
host = 'svc.sel5.cloudtype.app'
port = 32563
database = 'mes'

# Create a connection to the database
cnx = mysql.connector.connect(
    user=username,
    password=password,
    host=host,
    port=port,
    database=database
)

# Create a cursor object
cursor = cnx.cursor()

# Define the function to retrieve the values
def retrieve_values(input_value):
    query = "SELECT TITLE, 생산수량, 생산자, 생산일자, 검사방식, 표면처리여부, 타입, 불량, 오차수량, 제품위치, 작업자, 검사일자 FROM INPUT WHERE LOT = %s"
    cursor.execute(query, (input_value,))
    result = cursor.fetchall()
    return result

# Define the function to retrieve defect values
def retrieve_defect_values(lot):
    query = """
    SELECT 찍힘외형, 찍힘내형, 조도결, 척자국, 제품치수, 형상외형, 형상내경, 제품기스, 제품체결, 얼룩오염, 칩말림, 제품혼입, 제품분실, 
           샌딩찍힘외경, 샌딩찍힘내경, 샌딩조도결, 샌딩제품BURR, 샌딩제품치수, 샌딩형상외형, 샌딩형상내형, 샌딩제품기스, 
           샌딩제품라인, 샌딩탄자국, 샌딩이물외경, 표면처리미흡, 샌딩제품분실
    FROM INPUT WHERE LOT = %s
    """
    cursor.execute(query, (lot,))
    result = cursor.fetchall()
    return result

# Define the function to update the values in the database
def update_values(lot, updated_values, status):
    query = """
    UPDATE INPUT
    SET TITLE = %s, 생산수량 = %s, 생산자 = %s, 생산일자 = %s, 검사방식 = %s, 표면처리여부 = %s, 타입 = %s, 불량 = %s, 오차수량 = %s, 제품위치 = %s, 작업자 = %s, 검사일자 = %s, 검사현황 = %s
    WHERE LOT = %s
    """
    cursor.execute(query, (
        updated_values['TITLE'], updated_values['생산수량'], updated_values['생산자'], updated_values['생산일자'], updated_values['검사방식'], updated_values['표면처리여부'], updated_values['타입'],
        updated_values['불량'], updated_values['오차수량'], updated_values['제품위치'], updated_values['작업자'], updated_values['검사일자'], status, lot
    ))
    cnx.commit()

# Define the function to update defect values in the database
def update_defect_values(lot, defect_values):
    query = """
    UPDATE INPUT
    SET 찍힘외형 = %s, 찍힘내형 = %s, 조도결 = %s, 척자국 = %s, 제품치수 = %s, 형상외형 = %s, 형상내경 = %s, 제품기스 = %s, 제품체결 = %s, 얼룩오염 = %s, 칩말림 = %s, 제품혼입 = %s, 제품분실 = %s,
        샌딩찍힘외경 = %s, 샌딩찍힘내경 = %s, 샌딩조도결 = %s, 샌딩제품BURR = %s, 샌딩제품치수 = %s, 샌딩형상외형 = %s, 샌딩형상내형 = %s, 샌딩제품기스 = %s,
        샌딩제품라인 = %s, 샌딩탄자국 = %s, 샌딩이물외경 = %s, 표면처리미흡 = %s, 샌딩제품분실 = %s
    WHERE LOT = %s
    """
    cursor.execute(query, (
        defect_values['찍힘외형'], defect_values['찍힘내형'], defect_values['조도결'], defect_values['척자국'], defect_values['제품치수'], defect_values['형상외형'], defect_values['형상내경'], defect_values['제품기스'], defect_values['제품체결'], defect_values['얼룩오염'], defect_values['칩말림'], defect_values['제품혼입'], defect_values['제품분실'],
        defect_values['샌딩찍힘외경'], defect_values['샌딩찍힘내경'], defect_values['샌딩조도결'], defect_values['샌딩제품BURR'], defect_values['샌딩제품치수'], defect_values['샌딩형상외형'], defect_values['샌딩형상내형'], defect_values['샌딩제품기스'], defect_values['샌딩제품라인'], defect_values['샌딩탄자국'], defect_values['샌딩이물외경'], defect_values['표면처리미흡'], defect_values['샌딩제품분실'],
        lot
    ))
    cnx.commit()

# Define the function to retrieve worker list
def get_workers():
    query = "SELECT worker FROM INSPECTOR"
    cursor.execute(query)
    result = cursor.fetchall()
    return [worker[0] for worker in result]

# Define the function to retrieve location list
def get_locations():
    query = "SELECT 위치 FROM LOCATION"
    cursor.execute(query)
    result = cursor.fetchall()
    return [location[0] for location in result]

# Create a Streamlit app
st.title("Evidence Implant")

# CSS for layout adjustment
st.markdown(
    """
    <style>
    .reduce-space {
        display: flex;
        align-items: center;
        gap: 0.25rem;
    }
    .input-container {
        display: flex;
        align-items: center;
        gap: 1rem;
        margin-bottom: 1rem;
    }
    .input-container label {
        width: 150px;
        margin: 0;
    }
    .input-container input, .input-container select {
        flex: 1;
    }
    body {
        font-size: 14px;
        line-height: 1.2;
        padding: 10px;
    }
    .error-amount-container {
        font-size: 14px;
        line-height: 1.2;
        padding: 10px;
    }
    </style>
    """, unsafe_allow_html=True
)

st.markdown('<div class="reduce-space">LOT를 입력하세요.</div>', unsafe_allow_html=True)
input_value = st.text_input("", key="lot_input")

# Ensure inspection_date is set in session state
if "inspection_date" not in st.session_state:
    st.session_state.inspection_date = date.today()

# Ensure query result is set in session state
if "query_result" not in st.session_state:
    st.session_state.query_result = None

# Ensure defect values are set in session state
if "defect_values" not in st.session_state:
    st.session_state.defect_values = None

# Ensure defect form state is set in session state
if "show_defect_form" not in st.session_state:
    st.session_state.show_defect_form = False

# Fetch workers and locations from database
workers = get_workers()
locations = get_locations()

if st.button("조회"):
    if input_value:
        result = retrieve_values(input_value)
        st.session_state.query_result = result
        st.session_state.show_defect_form = False  # Reset defect form visibility on new query
    else:
        st.write("Please enter a value for LOT.")

if st.session_state.query_result:
    result = st.session_state.query_result
    if result:
        headers = ['TITLE', '생산수량', '생산자', '생산일자', '검사방식', '표면처리여부', '타입', '불량', '오차수량', '제품위치', '작업자', '검사일자']
        updated_values = {}

        # Create columns for left and right sections
        col1, col2 = st.columns(2)

        with col1:
            for i, row in enumerate(result):
                for header, data in zip(headers[:8], row[:8]):  # Left section: TITLE to 불량
                    st.markdown(f"""
                        <div class="input-container">
                            <label>{header}</label>
                            <input type="text" value="{data}" disabled>
                        </div>
                    """, unsafe_allow_html=True)
                    updated_values[header] = data

        with col2:
            for i, row in enumerate(result):
                for header, data in zip(headers[8:], row[8:]):  # Right section: 오차수량 to 검사일자
                    if header == '작업자':
                        selected_worker = st.selectbox(header, workers, index=workers.index(data) if data in workers else 0, key=f"worker_select_{i}")
                        updated_values[header] = selected_worker
                    elif header == '제품위치':
                        selected_location = st.selectbox(header, locations, index=locations.index(data) if data in locations else 0, key=f"location_select_{i}")
                        updated_values[header] = selected_location
                    elif header == '검사일자':
                        default_inspection_date = data if data else st.session_state.inspection_date
                        updated_inspection_date = st.date_input(header, value=default_inspection_date, key=f"inspection_date_{i}")
                        updated_values[header] = updated_inspection_date
                    else:
                        updated_values[header] = st.text_input(header, value=data, key=f"{header.lower()}_{i}")

        st.write("-" * 20)  # Adding a separator between rows

        if st.session_state.show_defect_form:
            defect_cols_1 = ['찍힘외형', '찍힘내형', '조도결', '척자국', '제품치수', '형상외형', '형상내경', '제품기스', '제품체결', '얼룩오염', '칩말림', '제품혼입', '제품분실']
            defect_cols_2 = ['샌딩찍힘외경', '샌딩찍힘내경', '샌딩조도결', '샌딩제품BURR', '샌딩제품치수', '샌딩형상외형', '샌딩형상내형', '샌딩제품기스', '샌딩제품라인', '샌딩탄자국', '샌딩이물외경', '표면처리미흡', '샌딩제품분실']

            if st.session_state.defect_values is None:
                st.session_state.defect_values = retrieve_defect_values(input_value)[0]
            defect_inputs = {}

            st.markdown("<h3>불량 세부사항</h3>", unsafe_allow_html=True)

            cols = st.columns(13)
            for i, (col, val) in enumerate(zip(defect_cols_1, st.session_state.defect_values[:13])):
                with cols[i]:
                    defect_inputs[col] = st.text_input(col, value=val, key=f"defect_{col}")

            cols = st.columns(13)
            for i, (col, val) in enumerate(zip(defect_cols_2, st.session_state.defect_values[13:])):
                with cols[i]:
                    defect_inputs[col] = st.text_input(col, value=val, key=f"defect_{col}")

            total_defect_value = sum(int(defect_inputs[col] or 0) for col in defect_cols_1 + defect_cols_2)
            st.text_input("총불량", value=total_defect_value, key="total_defect", disabled=True)

            if st.button("확인", key="confirm_defects"):
                updated_values['불량'] = total_defect_value
                st.session_state.show_defect_form = False
                st.session_state.query_result[0] = list(st.session_state.query_result[0])
                st.session_state.query_result[0][7] = total_defect_value  # Update the '불량' value in the session state
                
                # Update defect values in the database
                update_defect_values(input_value, defect_inputs)

                st.experimental_rerun()

        else:
            if st.button("불량 세부사항 입력", key="show_defects"):
                st.session_state.defect_values = retrieve_defect_values(input_value)[0]  # Fetch latest defect values
                st.session_state.show_defect_form = True
                st.experimental_rerun()

        # Create columns for horizontal button layout
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            if st.button("검사시작"):
                update_values(input_value, updated_values, "검사시작")
                st.info("Database updated with status: 검사시작")
        with col2:
            if st.button("MTP대기"):
                update_values(input_value, updated_values, "MTP대기")
                st.info("Database updated with status: MTP대기")
        with col3:
            if st.button("검사완료"):
                update_values(input_value, updated_values, "검사완료")
                st.info("Database updated with status: 검사완료")
        with col4:
            if st.button("출고대기"):
                update_values(input_value, updated_values, "출고대기")
                st.info("Database updated with status: 출고대기")

    else:
        st.write("No results found for the given LOT.")

# Close the cursor and the connection
cursor.close()
cnx.close()