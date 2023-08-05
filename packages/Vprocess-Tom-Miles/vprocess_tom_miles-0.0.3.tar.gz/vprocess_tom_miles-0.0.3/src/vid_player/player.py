import cv2


class VIDP:
    def __init__(self, pth):
        self.path = pth

    # @staticmethod
    def video_player(self):
        print(f'Your package function! \n {self.path}')


if __name__ == '__main__':
    video_player_object = VIDP('some/path.txt')
    video_player_object.video_player()