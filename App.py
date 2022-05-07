import streamlit as st
import mediapipe as mp
import numpy as np
import cv2
import time
import tempfile
from PIL import Image

mp_drawing = mp.solutions.drawing_utils
mp_face_mesh = mp.solutions.face_mesh

DEMO_IMAGE = 'demo.jpg'
DEMO_VIDEO = 'demo.mp4'



st.markdown(
    """
    <style>
    [data-testid= "stSidebar"][aria-expanded="true"] > div:first-child{
        width: 350px
    }
    [data-testid= "stSidebar"][aria-expanded="true"] < div:first-child{
        width: 350px
        margin-left: -350px
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.sidebar.title('Detection Configuration Sidebar')


@st.cache()
def image_resize(image, width=None, height=None, inter=cv2.INTER_AREA):
    dimension = None
    (h, w) = image.shape[:2]

    if width is None and height is None:
        return image
    if width is None:
        r = width / float(w)
        dimension = (int(w * r), height)

    else:
        r = width / float(w)
        dimension = (width, int(h * r))

    # Resize the Image and resize it so that it will fits to the dimension of the page
    resized = cv2.resize(image, dimension, interpolation=inter)

    return resized


app_mode = st.sidebar.selectbox('Choose the App Mode',
                                ['About App', 'Run on Image', 'Run on Video'])

if app_mode == 'About App':
    st.title('Face Mesh Detector App Using MediaPipe')
    st.markdown('In this Application we are using **MediaPipe** for Detection of Face Mesh')

    st.markdown(
        """ 
        <style>
        [data-testid= "stSidebar"][aria-expanded="true"] > div:first-child{
            width: 350px
        }
        [data-testid= "stSidebar"][aria-expanded="true"] > div:first-child{
            width: 350px
            
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    #st.video('https://youtu.be/o1lbR1EoQOM')

elif app_mode == 'Run on Image':
    drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)

    st.sidebar.markdown('---')
    st.markdown(
        """ 
        <style>
        [data-testid= "stSidebar"][aria-expanded="true"] > div:first-child{
            width: 350px
        }
        [data-testid= "stSidebar"][aria-expanded="true"] > div:first-child{
            width: 350px
            margin-left: -350px
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("**Detected Faces**")
    kpi1_text = st.markdown("0")

    max_faces = st.sidebar.number_input('Maximum No. of Faces', value=2, min_value=1)
    st.sidebar.markdown('---')
    detection_confidence = st.sidebar.slider('Min Detection Confidence', min_value=0.0, max_value=1.0, value=0.5)
    st.sidebar.markdown('---')

    img_file_buffer = st.sidebar.file_uploader("Upload an Image", type=["jpg", "jpeg", "png"])
    if img_file_buffer is not None:
        image = np.array(Image.open(img_file_buffer))

    else:
        demo_Image = DEMO_IMAGE
        image = np.array(Image.open(demo_Image))

    st.sidebar.text('Original Image')
    st.sidebar.image(image)

    face_count = 0

    ##Dashboard For Image

    with mp_face_mesh.FaceMesh(
            static_image_mode=True,
            max_num_faces=max_faces,
            min_detection_confidence=detection_confidence) as face_mesh:

        results = face_mesh.process(image)
        out_image = image.copy()

        ##Face Landmark Drawing
        for face_landmarks in results.multi_face_landmarks:
            face_count += 1

            mp_drawing.draw_landmarks(
                image=out_image,
                landmark_list=face_landmarks,
                connections=mp_face_mesh.FACE_CONNECTIONS,
                landmark_drawing_spec=drawing_spec)

            kpi1_text.write(f"<h1 style='text-align: center; color: red;'>{face_count}</h1>", unsafe_allow_html=True)
        st.subheader('Output Image')
        st.image(out_image, use_column_width=True)


elif app_mode == 'Run on Video':
    st.set_option('deprecation.showfileUploaderEncoding', False)

    use_webcam = st.sidebar.button('Use Webcam')
    record = st.sidebar.checkbox('Record Video')

    if record:
        st.markdown('**Recording in progress**')

    st.markdown(
        """ 
        <style>
        [data-testid= "stSidebar"][aria-expanded="true"] > div:first-child{
            width: 350px
        }
        [data-testid= "stSidebar"][aria-expanded="true"] > div:first-child{
            width: 350px
            margin-left: -350px
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    max_faces = st.sidebar.number_input('Maximum No. of Faces', value=5, min_value=1)
    st.sidebar.markdown('---')
    detection_confidence = st.sidebar.slider('Min Detection Confidence', min_value=0.0, max_value=1.0, value=0.5)
    st.sidebar.markdown('---')
    tracking_confidence = st.sidebar.slider('Min Tracking Confidence', min_value=0.0, max_value=1.0, value=0.5)
    st.sidebar.markdown('---')

    st.markdown("## Output")

    stframe = st.empty()

    video_file_buffer = st.sidebar.file_uploader("Upload a Video", type=['mp4', 'avi', 'flv', 'mov', 'asf', 'm4v'])
    tffile = tempfile.NamedTemporaryFile(delete=False)

    # We get our video inputs here
    # If no file is uploaded it will go for webcam
    if not video_file_buffer:
        # Here for Webcam
        if use_webcam:
            vid = cv2.VideoCapture(0)
        # esle it will play Demo video from here
        else:
            vid = cv2.VideoCapture(DEMO_VIDEO)
            tffile.name = DEMO_VIDEO
    else:
        tffile.write(video_file_buffer.read())
        vid = cv2.VideoCapture(tffile.name)

    width = int(vid.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
    get_fps = int(vid.get(cv2.CAP_PROP_FPS))

    # Recording
    codec = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')
    vid_output = cv2.VideoWriter('output1.mp4', codec, get_fps, (width, height))

    st.sidebar.text('Input Video')
    st.sidebar.video(tffile.name)

    fps_Out = 0
    i = 0

    drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)

    kpi1, kpi2, kpi3, kpi4 = st.beta_columns(4)

    with kpi1:
        st.markdown('**Frame Rate**')
        kpi1_text = st.markdown("0")

    with kpi2:
        st.markdown('**Detected Faces**')
        kpi2_text = st.markdown("0")

    with kpi3:
        st.markdown('**Width**')
        kpi3_text = st.markdown("0")

    with kpi4:
        st.markdown('**Height**')
        kpi4_text = st.markdown("0")


    st.markdown("<hr/>", unsafe_allow_html=True)

    ##Dashboard For Video

    with mp_face_mesh.FaceMesh(
            static_image_mode=True,
            max_num_faces=max_faces,
            min_detection_confidence=detection_confidence,
            min_tracking_confidence=tracking_confidence) as face_mesh:

        prevTime = 0

        while vid.isOpened():
            i += 1
            ret, frame = vid.read()
            if not ret:
                continue

            results = face_mesh.process(frame)
            frame.flags.writeable = True

            face_count = 0
            if results.multi_face_landmarks:
                ##Face Landmark Drawing
                for face_landmarks in results.multi_face_landmarks:
                    face_count += 1

                    mp_drawing.draw_landmarks(
                        image=frame,
                        landmark_list=face_landmarks,
                        connections=mp_face_mesh.FACE_CONNECTIONS,
                        landmark_drawing_spec=drawing_spec,
                        connection_drawing_spec=drawing_spec)

            # FPS Counter Logic
            currTime = time.time()
            fps = 1 / (currTime - prevTime)
            prevTime = currTime

            if record:
                vid_output.write(frame)
            ##Dashboard
            kpi1_text.write(f"<h1 style='text-align: center; color: red;'>{int(fps)}</h1>", unsafe_allow_html=True)
            kpi2_text.write(f"<h1 style='text-align: center; color: red;'>{face_count}</h1>", unsafe_allow_html=True)
            kpi3_text.write(f"<h1 style='text-align: center; color: red;'>{width}</h1>", unsafe_allow_html=True)
            kpi4_text.write(f"<h1 style='text-align: center; color: red;'>{height}</h1>", unsafe_allow_html=True)

            frame = cv2.resize(frame,(0,0), fx=0.8, fy=0.8)
            frame = image_resize(image= frame, width=640)
            stframe.image(frame, channels= 'BGR',use_column_width=True)


    st.text('Video Processed')
    output_video = open('output1.mp4', 'rb')
    output_bytes = output_video.read()
    st.video(output_bytes)

    vid.release()
    vid_output.release()
