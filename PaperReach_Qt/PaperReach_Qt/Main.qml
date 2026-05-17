import QtQuick
import QtQuick.Window
import QtQuick.Controls
import QtQuick.Layouts
import Qt5Compat.GraphicalEffects

Window {
    id: root
    width: 1400
    height: 900
    visible: true
    title: qsTr("PaperReach")

    // Fensterhintergrund unsichtbar machen
    color: "transparent"
    flags: Qt.FramelessWindowHint | Qt.Window // Window Hint hinzugefügt, damit es in der Taskleiste bleibt




    // Das Haupt-Container-Rectangle (damit der Schatten Platz hat)
    Rectangle {
        id: mainBackground
        anchors.fill: parent
        anchors.margins: 15
        color: "#f5f5f5"    // Hintergrundfarbe der App
        radius: 10

        // titelleiste ist Buggy: ist aber ok für jetzt... :/
        Rectangle {
            id: mainContent
            anchors.fill: parent
            anchors.margins: 0
            color: "#f0f0f0"
            radius: 10

            //  TITELLEISTE
            Rectangle {
                id: titleBar
                width: parent.width
                height: 40
                color: "transparent"
                radius: 10
                anchors.top: parent.top

                // Verhindert, dass die unteren Ecken auch rund sind
                Rectangle {
                    anchors.bottom: parent.bottom
                    width: parent.width
                    height: parent.height / 2
                    color: parent.color
                    z: -1
                }

                //Text {
                //    text: "PaperReach"
                //    color: "white"
                //    anchors.centerIn: parent
                //}

                // Qt 6 DragHandler
                DragHandler {
                    onActiveChanged: if (active) root.startSystemMove()
                }

                // Schließen Button
                //Button {
                //    text: "✕"
                //    anchors.right: parent.right
                //    anchors.verticalCenter: parent.verticalCenter
                //    anchors.rightMargin: 10
                //    width: 30; height: 30
//
                //    onClicked: root.close() // Schließt die Applikation
//
                //    background: Rectangle {
                //        color: parent.down ? "#aa3333" : (parent.hovered ? "#ff4444" : "transparent")
                //        radius: 5
                //    }
                //}
            }
        }

        // Schatten
        DropShadow {
            anchors.fill: mainBackground
            horizontalOffset: 0
            verticalOffset: 2
            radius: 12.0
            samples: 25
            color: "#40000000"
            source: mainBackground
            z: -1 // Hinter dem Inhalt zeichnen
        }

        // --- wenn kein Bock auf schatten, einfach nur das nehmen :) ---
        RowLayout {
            anchors.fill: parent
            spacing: 15
            anchors.margins: 15

            Rectangle { // Linke Seite
                id: leftPanel
                Layout.preferredWidth: 500
                Layout.fillHeight: true
                color: "#ffffff"
                border.color: "#e6e6e6"
                radius: 8

                ColumnLayout {
                    anchors.top: parent.top
                    anchors.left: parent.left
                    anchors.right: parent.right
                    height: parent.height / 2
                    spacing: 15
                    anchors.margins: 20

                    TextArea {
                        id: inputField
                        Layout.fillWidth: true
                        Layout.fillHeight: true
                        placeholderText: "Ihre Notizen hier..."
                        background: Rectangle {
                            color: "#fcfcfc"
                            border.color: inputField.activeFocus ? "#3a86ff" : "#e6e6e6"
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
                        onClicked: backend.make_query(inputField.text)
                    }

                    Text {
                        text: "Sources"
                        font.pointSize: 10
                        font.weight: Font.Medium
                        color: "#7f8c8d"
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

                Rectangle { // Links unten
                    anchors.bottom: parent.bottom
                    anchors.left: parent.left
                    anchors.right: parent.right
                    anchors.margins: 10
                    height: parent.height / 2 - 60
                    color: "#f9f9f9"
                    border.color: "#e6e6e6"
                    radius: 8

                    Text {
                        anchors.centerIn: parent
                        text: "Querys werden hier angezeigt"
                        color: "#616161"
                        visible: backend.query_result === ""
                    }

                    ScrollView {
                        id: resultScroll
                        anchors.fill: parent
                        anchors.margins: 10
                        clip: true 
                        ScrollBar.vertical.policy: ScrollBar.AsNeeded

                        Text {
                            
                            width: resultScroll.availableWidth //breite an scrollview anpassen

                            text: backend.query_result
                            lineHeight: 1.4
                            color: '#191818'
                            wrapMode: Text.WordWrap

                            horizontalAlignment: Text.AlignHCenter
                            verticalAlignment: Text.AlignVCenter

                            height: Math.max(resultScroll.availableHeight, implicitHeight)
                        }
                    }

                }
            }

            Rectangle { // Rechte Seite
                Layout.fillWidth: true
                Layout.fillHeight: true
                color: "#ffffff"
                border.color: "#e6e6e6"
                radius: 8
                clip: true

                ColumnLayout {
                    anchors.fill: parent
                    spacing: 0

                    // gedrücktes Paper Element von unten (1/3 der Höhe)
                    Rectangle {
                        id: infoBlock
                        Layout.fillWidth: true
                        Layout.preferredHeight: parent.height / 3
                        color: "#fdfdfd" // Leicht abgesetzte Farbe
                        border.color: "#eeeeee"
                        Text {
                            anchors.centerIn: parent
                            text: "Zusatzinfos erscheinen hier"
                            color: "#95a5a6"
                            font.italic: true
                        }

                        // Trennlinie zum unteren Block
                        Rectangle {
                            anchors.bottom: parent.bottom
                            width: parent.width
                            height: 1
                            color: "#e6e6e6"
                        }
                    }

                    // Alle Paper (2/3 der Höhe)
                    ColumnLayout {
                        Layout.fillWidth: true
                        Layout.fillHeight: true
                        spacing: 15
                        Layout.margins: 20

                        Text {
                            text: "Ergebnisse in relation zum eingegebenen Text:"
                            font.pointSize: 12
                            font.weight: Font.Medium
                            color: "#7f8c8d"
                        }

                        ScrollView {
                            Layout.fillWidth: true
                            Layout.fillHeight: true
                            clip: true
                            ScrollBar.vertical.policy: ScrollBar.AsNeeded

                            ListView {
                                id: resultList
                                spacing: 10
                                model: paperModel
                                width: parent.width // Wichtig für die Breite der Delegates

                                delegate: Rectangle {
                                    width: resultList.width
                                    height: 150 
                                    color: "#fcfcfc"
                                    border.color: "#eeeeee"
                                    radius: 6
                                    // Tipp-geste hinzufügen

                                    MouseArea {
                                        anchors.fill: parent
                                        onClicked: {
                                            // Hier später die Logik für exra Info
                                            console.log("Gedrückt auf Index: " + index)
                                        }
                                    }

                                    ColumnLayout {
                                        anchors.fill: parent
                                        anchors.margins: 15


                                        Text {
                                            text: title
                                            color: '#2a2a2a'
                                            
                                        }

                                        Text {
                                            text: abstract
                                            wrapMode: Text.WordWrap
                                            Layout.fillWidth: true
                                            color: '#424242'
                                            elide: Text.ElideRight
                                            maximumLineCount: 3
                                        }

                                        Text {
                                            text: "Rating: " + rating
                                            color: Qt.rgba(
                                                (100 - rating) / 100, // Rotanteil
                                                rating / 100,           // Grünanteil
                                                0,                      // Blauanteil
                                                1.0
                                            )
                                            font.italic: true
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}