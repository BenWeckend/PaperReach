import QtQuick
import QtQuick.Window
import QtQuick.Controls
import QtQuick.Layouts

Window {
    width: 1100
    height: 800
    visible: true
    title: qsTr("PaperReach")

    RowLayout {
        anchors.fill: parent
        spacing: 5
        anchors.margins: 15
        anchors.topMargin: 20


        Rectangle {
            Layout.preferredWidth: 500
            Layout.fillHeight: true
            color: "#ffffff"
            border.color: "#e6e6e6"
            radius: 8 // Sanftere Ecken

            ColumnLayout {
                // Wir nehmen nur die obere Hälfte ein
                anchors.top: parent.top
                anchors.left: parent.left
                anchors.right: parent.right
                height: parent.height / 2

                spacing: 15
                anchors.margins: 20

                TextArea { // TextArea statt TextField für größere Eingaben
                    id: inputField
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                    placeholderText: "Ihre Notizen hier..."
                    background: Rectangle {
                        color: "#fcfcfc"
                        border.color: inputField.activeFocus ? "#3a86ff" : "#e6e6e6" // hover Effekt -> mega cool
                        radius: 4
                    }
                    wrapMode: Text.WordWrap

                }

                Button {
                    text: "Search"
                    Layout.fillWidth: true
                    Layout.preferredHeight: 40

                    contentItem: Text {
                        text: parent.text
                        font.weight: Font.DemiBold
                        color: "white"
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                    }

                    background: Rectangle {
                        color: parent.down ? "#2a6edb" : (parent.hovered ? "#4a96ff" : "#3a86ff")
                        radius: 4
                    }
                }
            }

            Rectangle {  // Mitte 2
                anchors.bottom: parent.bottom
                anchors.left: parent.left
                anchors.right: parent.right
                height: parent.height / 2 - 40

                border.color: "#e6e6e6"
                radius: 8
            }
        }



        Rectangle {  // Rechts
            Layout.fillWidth: true
            Layout.fillHeight: true
            color: "#ffffff"
            border.color: "#e6e6e6"
            border.width: 1
            radius: 8
        }
    }
}
