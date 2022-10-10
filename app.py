from PIL import Image
import shortuuid
import urllib
import requests
import streamlit as st
from streamlit_lottie import st_lottie
from streamlit_option_menu import option_menu
import streamlit_nested_layout
st.set_page_config(page_title='Coin x Bay', page_icon=':zap:', layout='wide')

#region --- AIRTABLE ---
AIRTABLE_BASE_ID='app72nm0PCRYJwQxG'
AIRTABLE_API_KEY='key1UL3uPAYNJcuVV'
AIRTABLE_TABLE_NAME='products-listing'
endpoint=f'https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{AIRTABLE_TABLE_NAME}'

def add_to_airtable():
    if st.session_state.title is None:
        return
    st.session_state.orderID = shortuuid.uuid()
    headers = {
        "Authorization": f"Bearer {AIRTABLE_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
    "records": [
            {
            "fields": {
                "order-id": st.session_state.orderID,
                "product": st.session_state.title,
                "url": st.session_state.my_input,
                "variations": st.session_state.variation,
                "variation-details": st.session_state.variationdets,
                'amount': str(st.session_state.amount),
                "name": st.session_state.name,
                "address": st.session_state.address
                }
            }
        ]
    }
    r = requests.post(endpoint, json=data, headers=headers)
    if r.status_code == 200:
        orderCompleted()
#endregion

#region --- CSS ---
def css(filename):
    with open(filename) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
css(r"style.css")
#endregion

#region --- SESSION MANAGERS --- 
def startSess():
    st.session_state.submitted = False
    st.session_state.imgprevurl = None
    st.session_state.my_input = None
    st.session_state.expand = True
    st.session_state.payment = False
if 'submitted' not in st.session_state:
    startSess()
def buyPanel():
    if st.session_state['submitted']:
        st.session_state.expand = True
        st.session_state.submitted = False
    else:
        st.session_state.expand = False
        st.session_state.submitted = True
def buy():
    st.session_state.payment = True
def closeBuyPanel():
    st.session_state.payment = False
def orderCompleted():
    st.session_state.payment = True
    st.session_state.submitted = False
def newOrder():
    st.session_state.payment = False
    st.session_state.submitted = False
    for key in st.session_state.keys():
        del st.session_state[key]
    startSess()
#endregion

#region --- MENU ---
st.write('<style>div.block-container{padding-top:0rem;margin-top:-2rem}</style>', unsafe_allow_html=True)
selected = option_menu (
    menu_title = None , #required
    options = [ "HOME" , "TRACK ORDER" , "SUPPORT" ] , #required
    icons = [ "house" , "search" , "envelope" ] , #optional
    menu_icon = "cast" , #optional
    default_index = 0 , #optional
    orientation='horizontal',
        styles={
        "container": {"padding": "0!important",'border-radius': '0px','background-image': "radial-gradient( circle farthest-corner at 10% 20%,  rgba(0,221,214,1) 0%, rgba(51,102,255,1) 90% )",},
        "icon": {"color": "white", "font-size": "25px"}, 
        "nav-link": {"font-size": "25px", "text-align": "left", "margin":"0px", "--hover-color": "#0060a1", "text-align": "center",'border-radius': '20px'},
        "nav-link-selected": {'background-image': "radial-gradient( circle farthest-corner at 10% 20%,  rgba(0,221,214,1) 0%, rgba(51,102,255,1) 90% )","font-size": "0px",'border-radius': '20px'},
    }
)
#endregion

#region --- LOAD ASSESTS --- 
@st.cache(show_spinner=False)
def get_url(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

@st.cache(show_spinner=False)
def load_assets():
    lottie_code = get_url('https://assets7.lottiefiles.com/packages/lf20_l5qvxwtf.json')
    lottie_load = get_url('https://assets4.lottiefiles.com/packages/lf20_8PpfJUolaj.json')
    img_1 = Image.open(r"images\FocusPal-1.png")
    header_logo = Image.open(r"images\headerlogo.png")
    return lottie_code,lottie_load,img_1,header_logo

lottie_code,lottie_load,img_1,header_logo = load_assets()
#endregion

#region --- HOME TAB ---
if selected == 'HOME':
    with st.container():
        # New Order Page
        if not st.session_state.submitted and not st.session_state.payment:
            expander = st.expander(label='',expanded=st.session_state.expand)
            st.session_state.imgprevurl = None
            expander.write('##')
            expander.image(
                'https://i.ibb.co/CVbJjw9/headerlogo.png',
                width=200, # Manually Adjust the width of the image as per requirement
            )
            #expander.subheader ("CoinxBay")
            expander.markdown("""
            <span style='font-weight:bold;font-style:italic;font-family:"Century Gothic";'><span style='color:#00DDD6;'>B</span><span style='color:#02D7D7;'>U</span><span style='color:#04D2D9;'>Y</span> <span style='color:#08C8DD;'>A</span><span style='color:#0BC3DE;'>N</span><span style='color:#0DBDE0;'>Y</span><span style='color:#0FB8E2;'>T</span><span style='color:#11B3E4;'>H</span><span style='color:#13AEE6;'>I</span><span style='color:#16A9E7;'>N</span><span style='color:#18A4E9;'>G</span><span style='color:#1A9EEB;'>,</span> <span style='color:#1F94EE;'>A</span><span style='color:#218FF0;'>N</span><span style='color:#238AF2;'>Y</span><span style='color:#2585F4;'>W</span><span style='color:#277FF6;'>H</span><span style='color:#2A7AF7;'>E</span><span style='color:#2C75F9;'>R</span><span style='color:#2E70FB;'>E</span><span style='color:#306BFD;'>,</span></span>
            """, unsafe_allow_html=True)
            expander.markdown("""
            <span style='font-weight:bold;font-style:italic;font-family:"Century Gothic";'><span style='color:#00DDD6;'>W</span><span style='color:#04D2D9;'>I</span><span style='color:#09C7DD;'>T</span><span style='color:#0DBCE1;'>H</span> <span style='color:#17A6E8;'>C</span><span style='color:#1B9CEC;'>R</span><span style='color:#2091F0;'>Y</span><span style='color:#2586F3;'>P</span><span style='color:#297BF7;'>T</span><span style='color:#2E70FB;'>O</span></span>
            """, unsafe_allow_html=True)
            expander.write('## Easy | Safe | Private')
            expander.write('## \n##')
            expander.markdown("""
            <span style='font-family:"Century Gothic";'><span style='color:#667EEA;'>E</span><span style='color:#667BE6;'>n</span><span style='color:#6778E2;'>t</span><span style='color:#6875DE;'>e</span><span style='color:#6973DA;'>r</span> <span style='color:#6B6DD3;'>P</span><span style='color:#6B6BCF;'>r</span><span style='color:#6C68CB;'>o</span><span style='color:#6D65C7;'>d</span><span style='color:#6E63C4;'>u</span><span style='color:#6F60C0;'>c</span><span style='color:#705DBC;'>t</span> <span style='color:#7158B4;'>L</span><span style='color:#7255B1;'>i</span><span style='color:#7353AD;'>n</span><span style='color:#7450A9;'>k</span><span style='color:#754DA5;'>:</span></span>
            """, unsafe_allow_html=True)
            if "my_input" not in st.session_state:
                st.session_state.my_input = ""
            my_input = expander.text_input(" ", placeholder = ' Product Link from Any Website (eBay, Etsy, Lazada, etc.)')
            expander.write('##')
            a, b, c,d,e = expander.columns(5)
            with c:
                if my_input == '' or my_input == None:
                    disabledFlag = True
                else:
                    st.session_state.my_input = my_input
                    disabledFlag = False
                submit = st.button("Buy with Crypto", on_click=buyPanel, key="show",disabled=disabledFlag)
                expander.write('##')

            st.write('##')

            # --- HOW IT WORKS ---
            with st.container():
                st.write("---")
                left_column, right_column = st.columns(2)
                with left_column:
                    st.title("How it works")
                    st.write('##')
                    st.write('magiccc pizazzz')
                with right_column:
                    st_lottie(lottie_code, height=300, key="lottieanim")
                    #st.markdown('<iframe src="https://embed.lottiefiles.com/animation/83717"></iframe>',unsafe_allow_html=True)
            # --- MORE ---
            with st.container():
                st.write("---")
                st.title("How it works")
                st.write('##')
                img_column, text_column = st.columns((1,2))
                with img_column:
                    st.subheader('Img here...')
                    st.image(img_1)
                with text_column:
                    st.subheader('More Searcht things')
                    st.write('ok jz filling tings')
                    st.markdown ("[Learn More](/Buy_Page)")
        
        # Buy Page
        elif st.session_state.submitted and not st.session_state.payment:
            if st.session_state.imgprevurl == None:
                lottie_container = st.empty()
                with lottie_container:
                    loading_lottie = st_lottie(lottie_load, height=700, key="loading_lottie")
            try:
                st.session_state.url = urllib.parse.quote(st.session_state.my_input)
                preview = get_url(f'https://metagrabber.vercel.app/api?url={st.session_state.url}')
                try:
                    lottie_container.empty()
                except:
                    pass
                st.session_state.title = preview['title']
                st.session_state.desc = preview['description']
                st.session_state.imgprevurl = preview['image'] 

                # Line break with less gap
                lineexp = st.expander(label='',expanded=False)
                lineexp.write(' ')

                st.write('##')
                buycols = st.columns((2,3))
                with buycols[0]:
                    st.image(
                        st.session_state.imgprevurl,
                        width=460, # Manually Adjust the width of the image as per requirement
                    )

                with buycols[1]:
                    titleexpander = st.expander(label='',expanded=True)
                    titleexpander.subheader(st.session_state.title)
                    varcols = st.columns(3)
                    with varcols[0]:
                        st.subheader('Select Variation:')
                    with varcols[1]:
                        st.session_state.variation = st.radio(
                            "Set Variation:",
                            ["Default", "Custom"],
                            label_visibility='collapsed',
                            disabled=False,
                            horizontal=True
                        )  
                    if st.session_state.variation == 'Custom':
                        st.session_state.variationdets = st.text_input(label='Enter Your Custom Variations:',placeholder=' Example: White, XL, long-sleeves, etc.')
                        st.write('###')
                        if st.session_state.variationdets == '':
                            buydisabled = True
                        else:
                            buydisabled = False
                    else:
                        st.session_state.variationdets = ''
                        buydisabled = False
                    numcols = st.columns(3)
                    with numcols[0]:
                        st.subheader('Select Amount:')
                    with numcols[1]:
                        st.session_state.amount = st.number_input(label=' ', label_visibility='collapsed',min_value=1, format='%i')
                    st.write('##')
                    butcols = st.columns((1,1,1))
                    with butcols[0]:
                        st.button('Buy', on_click=buy, key="buy",disabled=buydisabled)
                    with butcols[1]:
                        st.markdown(f'''
                            <a target="_blank" href="{st.session_state.my_input}">
                                <button kind="primary" class="css-r0ncp3 edgvbvh9" style="margin-bottom: 1rem;">
                                    Product Details
                                </button>
                            </a>
                            ''',
                            unsafe_allow_html=True
                        )
                    with butcols[2]:
                        cancel = st.button('Cancel', on_click=buyPanel, key="close")
                        if cancel:
                            st.session_state.imgprevurl = None
                            print('cancel')
                st.write('##')
            except:
                try:
                    lottie_container.empty()
                except:
                    pass
                cancelcols = st.columns(3)
                with cancelcols[1]:
                    st.write('##')
                    st.write('##')
                    st.title('Error!\nPlease Return & Retry')
                    st.write('##')
                    st.button('Return', on_click=buyPanel, key="return")
        
        # Delivery Details Page
        elif st.session_state.submitted and st.session_state.payment:
            with st.container():
                # Line break with less gap
                lineexp = st.expander(label='',expanded=False)
                lineexp.write(' ')
                paycols = st.columns((1,3))
                with paycols[0]:
                    detsexpander = st.expander(label='',expanded=True)
                    detsexpander.write('###')
                    detsexpander.image(
                        st.session_state.imgprevurl,
                        width=300, # Manually Adjust the width of the image as per requirement
                    )
                    detsexpander.write('#### '+st.session_state.title)
                    detsexpander.write('#### '+'Variations:')
                    if st.session_state.variation == 'Default':
                        detsexpander.write('##### Default')
                    else:
                        detsexpander.write('##### '+ st.session_state.variationdets)
                    detsexpander.write('#### '+'Amount:')
                    detsexpander.write('##### '+ str(st.session_state.amount))
                with paycols[1]:
                    st.title('Enter Delivery Details')
                    st.subheader('Name (Alias):')
                    st.text_input(label=' ', label_visibility='collapsed',key = 'name')
                    st.subheader('Delivery Address:')
                    st.text_input(label=' ', label_visibility='collapsed', key='address')
                    st.write('##')
                    paymentcols = st.columns(3)
                    with paymentcols[2]:
                        if st.session_state.name != '' and st.session_state.address != '':
                            paymentDisabled = False
                        else:
                            paymentDisabled = True                        
                        st.button('Proceed to Payment', on_click=add_to_airtable, key="pay",disabled=paymentDisabled)
                        cancel = st.button('Back', on_click=closeBuyPanel, key="back")
        
        # Order Completed Page
        elif not st.session_state.submitted and st.session_state.payment:
            # Line break with less gap
            lineexp = st.expander(label='',expanded=False)
            lineexp.write(' ')
            with st.container():
                paycols = st.columns((1,3))
                with paycols[0]:
                    detsexpander = st.expander(label='',expanded=True)
                    detsexpander.write('###')
                    detsexpander.image(
                        st.session_state.imgprevurl,
                        width=300, # Manually Adjust the width of the image as per requirement
                    )
                    detsexpander.write('#### '+st.session_state.title)
                    detsexpander.write('#### '+'Variations:')
                    detsexpander.write('##### '+st.session_state.variation)
                    detsexpander.write('#### '+'Amount:')
                    detsexpander.write('##### '+ str(st.session_state.amount))
                with paycols[1]:
                    st.title('Order Successfully Submitted!')
                    st.write('##  \n##')
                    st.subheader(f'Order ID: {st.session_state.orderID}'+"\n###### ( Please save your Order ID, it won't be shown again. This is the ONLY way to track your order. )")
                    st.write('## \n## \n## \n## \n# \n#### \n####  ')
                    newordcols = st.columns(3)
                    with newordcols[2]:
                        st.button('Add New Order', on_click=newOrder, key="neworder")
#endregion

#region --- TRACK TAB ---
elif selected == 'TRACK ORDER':
    with st.container():
        # Line break with less gap
        lineexp = st.expander(label='',expanded=False)
        lineexp.write(' ')
#endregion

#region --- SUPPORT TAB ---
elif selected == 'SUPPORT':
    with st.container():
        # Line break with less gap
        lineexp = st.expander(label='',expanded=False)
        lineexp.write(' ')

        st.title("Contact Support")
        st.write('##')
        # Documention: https://formsubmit.co/ !!! CHANGE EMAIL ADDRESS !!!
        contact_form = """
        <form action="https://formsubmit.co/lingaiswaran@gmail.com" method="POST">
            <input type= "hidden" name="_captcha" value="false">
            <input type= "text" name= "name" placeholder="Your name" required>
            <input type="email" name="email" placeholder="Your email" required>
            <textarea name= "message" placeholder= "Your message here" required></textarea>
            <button kind="primary" class="css-r0ncp3 edgvbvh9" style="margin-top: 1rem;">Send</button>
        </form>
        """
        suppcols = st.columns(3)
        with suppcols[1]:
            st.markdown(contact_form, unsafe_allow_html=True)
#endregion
