from kivy.app import App
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
import cv2
class QRApp(App):
	def build(self):
		bl = BoxLayout(orientation = 'vertical')
		self.img=Image(allow_stretch=True, keep_ratio=False)
		self.lbl=Label(padding = 5)#size_hint = (1,.2))
		self.scrl = ScrollView(size_hint=(1, .3), do_scroll_x=False)
		def on_width(widget, size):
			self.img.height = size
		def on_size(widget, size):
			self.lbl.texture_update()
			self.lbl.font_size = int(min(size)*0.2)
			self.lbl.text_size = (self.lbl.width, None)
			if self.lbl.texture_size[1] > self.lbl.height:
				new_height = self.lbl.texture_size[1]
				self.lbl.height = new_height
				self.scrl.scroll_y = 0
		self.capture = cv2.VideoCapture(1)
		fps = 30
		Clock.schedule_interval(self.update, 1.0/fps)
		self.lbl.bind(size=on_size)
		self.img.bind(width=on_width)
		self.scrl.add_widget(self.lbl)
		bl.add_widget(self.img)
		bl.add_widget(self.scrl)
		return bl
	def update(self, fps):
		ret, frame = self.capture.read()
		self.qcd = cv2.QRCodeDetector()
		text_qr = 'наведите камеру на qr-код'
		if ret:
			ret_qr, decoded_info, points, _ = self.qcd.detectAndDecodeMulti(frame)
			if ret_qr:
				for q,p in zip(decoded_info,points):
					if q:
						text_qr = 'текст с qr-кода:\n' + str(q)
						color = (0, 255, 0)
					else:
						color = (0, 0, 255)
					frame = cv2.polylines(frame, [p.astype(int)], True, color, 8)
			buf1 = cv2.flip(frame, 0)
			buf = buf1.tostring()
			image_texture = Texture.create(size = (frame.shape[1], frame.shape[0]), colorfmt = 'bgr')
			image_texture.blit_buffer(buf, colorfmt = 'bgr', bufferfmt = 'ubyte')
			#print(text_qr)
			self.lbl.text = text_qr
			self.img.texture = image_texture
	def on_stop(self):
		self.capture.release()
if __name__ == '__main__':
    QRApp().run()