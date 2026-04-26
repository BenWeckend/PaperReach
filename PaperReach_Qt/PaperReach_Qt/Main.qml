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


        Rectangle { // ganze linke Seite
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

                // Hauptüberschrift
                //Text {
                //    text: "Search Options"
                //    font.pointSize: 12
                //    font.weight: Font.Bold
                //    color: "#003975"
                //    Layout.topMargin: 10
                //}

                // Unterüberschrift
                Text {
                    text: "Sources"
                    font.pointSize: 10
                    font.weight: Font.Medium
                    color: "#7f8c8d"
                    Layout.topMargin: 5
                }

                RowLayout {
                    Layout.fillWidth: true
                    spacing: 20

                    // blaues Design
                    component BlueCheckBox : CheckBox {
                        id: control
                        indicator: Rectangle {
                            implicitWidth: 20
                            implicitHeight: 20
                            x: control.leftPadding
                            y: parent.height / 2 - height / 2
                            radius: 4
                            border.color: control.checked ? "#3a86ff" : "#e6e6e6"
                            color: control.checked ? "#3a86ff" : "transparent"

                            // Das Häkchen
                            Rectangle {
                                width: 10
                                height: 10
                                x: 5
                                y: 5
                                radius: 2
                                color: "white"
                                visible: control.checked
                            }
                        }
                    }

                    BlueCheckBox {
                        id: semScol
                        text: "Semantic Scholar"
                        checked: true
                        onCheckedChanged: console.log("Semantic Scholar " + checked)
                    }

                    BlueCheckBox {
                        id: arXiv
                        text: "arXiv"
                        checked: true
                        onCheckedChanged: console.log("arXiv " + checked)
                    }
                }

            }

            Rectangle {  // links unten
                anchors.bottom: parent.bottom
                anchors.left: parent.left
                anchors.right: parent.right
                height: parent.height / 2 - 40

                border.color: "#e6e6e6"
                radius: 8

                Text {
                    text: "Generated Queries"
                    font.pointSize: 12
                    font.weight: Font.Medium
                    color: "#616161"
                    Layout.topMargin: 10

                }
                Text { // Liste an generierten Queries ausgeben
                    id: outputTextQueries
                    text: "Ausgabe erscheint hier"
                }


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
